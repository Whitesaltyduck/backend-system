from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres:fenster123@localhost:5432/backend_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
