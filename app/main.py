from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db import engine, SessionLocal
from app.models import Base, Note, User
from app.schemas import NoteCreate, NoteOut, UserCreate, Token
from app.security import verify_password, hash_password
from app.auth import create_access_token, decode_access_token

app = FastAPI()

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

security = HTTPBearer(auto_error=False)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    if not credentials:
        raise HTTPException(status_code=401, detail="Authentication required")

    payload = decode_access_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

def require_admin(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

def get_optional_admin(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: Session = Depends(get_db)
):
    user_count = db.query(User).count()

    if user_count == 0:
        return None

    if not credentials:
        raise HTTPException(status_code=401, detail="Authentication required")

    payload = decode_access_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == int(payload.get("sub"))).first()
    if not user or user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    return user

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/users")
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_admin)
):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    existing_users = db.query(User).count()

    db_user = User(
        email=user.email,
        hashed_password=hash_password(user.password),
        role="admin" if existing_users == 0 else "user"
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"id": db_user.id, "email": db_user.email}

@app.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/notes", response_model=NoteOut)
def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    db_note = Note(title=note.title, content=note.content)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@app.get("/notes", response_model=list[NoteOut])
def get_notes(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return db.query(Note).all()
