# Backend System – Azure DevOps (AZ-400 Project)

This project was built to gain **hands-on experience with Azure DevOps (AZ-400)** concepts,
with a focus on **CI/CD pipelines, Infrastructure as Code (IaC), authentication, and cloud
runtime debugging**.

The objective was not application complexity, but understanding **how real delivery systems
behave**, how they fail, and how they are responsibly operated and decommissioned.

---

## Problem Statement

Most cloud backend failures are caused not by application logic,
but by misconfigured CI/CD pipelines, identity mismatches,
environment drift, and incorrect assumptions about cloud runtimes.

This project investigates those failure modes by building,
deploying, breaking, debugging, and decommissioning a
production-style backend system on Azure.

---

## Project Intent

This project emphasizes:

- CI/CD over feature development
- Infrastructure reproducibility
- Identity and configuration correctness
- Failure analysis and debugging
- Full lifecycle ownership (create → operate → destroy)

The project is intentionally **closed** after achieving learning goals
to avoid unnecessary cloud costs and scope creep.

---

## Tech Stack

- **Backend**: FastAPI (Python)
- **Hosting**: Azure App Service (Linux)
- **CI/CD**: GitHub Actions
- **Infrastructure as Code**: Bicep
- **Authentication**: JWT / OIDC
- **Database**: Azure PostgreSQL Flexible Server (tested, later decommissioned)
- **Monitoring**: Azure App Service logs, GitHub Actions logs
- **Region**: Malaysia West (Azure Student subscription constraint)

---

## High-Level Architecture

<img width="1024" height="559" alt="image" src="https://github.com/user-attachments/assets/2bbd9ab9-2d3c-4891-bded-b8fb5da33005" />

*Figure 1: High-level architecture showing the flow from GitHub (source of truth) through
GitHub Actions CI/CD into Azure App Service hosting a FastAPI application, with PostgreSQL as
an external managed dependency used during development.*

### Diagram Description

The system follows a standard DevOps delivery flow:

- GitHub repository is the **single source of truth**
- GitHub Actions builds and deploys the application
- Azure App Service runs the FastAPI backend
- PostgreSQL is an external managed dependency (used during testing phase)
- Logs provide feedback during failures

---

## Logical Flow

<img width="1024" height="559" alt="image" src="https://github.com/user-attachments/assets/1a73561b-fa71-4c03-8107-6a4cdc2000eb" />

*Figure 2: Logical flow illustrating how a source code push to GitHub triggers GitHub Actions
pipelines, resulting in application deployment to Azure App Service and execution within the
FastAPI runtime.*

> **Key principle learned:**  
> A successful pipeline deploys artifacts — it does **not** guarantee a healthy runtime.

---

## Repository Structure

<img width="1024" height="559" alt="image" src="https://github.com/user-attachments/assets/71b25e64-7e26-4318-8a98-ba13080d6d09" />

*Figure 3: Repository structure highlighting separation of concerns between application code
(`app/`), infrastructure as code (`infra/` using Bicep), and CI/CD pipelines
(`.github/workflows`).*

---

## Infrastructure as Code (IaC)

Infrastructure is defined using **Bicep** to ensure reproducibility and controlled
provisioning.

### Defined Resources
- App Service Plan (B1)
- Linux App Service (Python runtime)

### IaC File
- `infra/appservice.bicep`

### Deployment Command
```bash
- az deployment group create --resource-group rg-backend-iac --template-file infra/appservice.bicep
```

Important distinction:
- IaC defines **infrastructure shape**
- Secrets, credentials, and identity are **intentionally excluded**

---

## Application Surface (Minimal)

The backend exposes a deliberately small API surface to support  
authentication, authorization, and operational validation.

- `GET /health`  
  Validates service readiness and dependency availability

- `POST /users`  
  Bootstrap user creation and RBAC validation

- `POST /login`  
  JWT token issuance and identity verification

- `POST /notes`, `GET /notes`  
  Protected routes used to validate authentication enforcement

The API exists to **support system behavior**, not to model a business domain.

---

## Local Reproduction

This system can be executed locally to validate application behavior  
independent of Azure infrastructure.

### Steps

1. Create a Python virtual environment  
2. Install dependencies from `requirements.txt`  
3. Define required environment variables  
4. Start the application  
5. Verify `/health`

> **Configuration Model**
>
> Local development uses an `.env` file loaded by the application server.  
> In production, configuration is injected by the platform.  
> The application code does not load environment files directly.

---

## Health Semantics

The `/health` endpoint represents **service readiness**, not mere process liveness.

It validates:
- application startup
- database connectivity

A successful CI/CD deployment does not imply runtime readiness;  
this endpoint exists to explicitly verify that distinction.

---

## CI/CD Pipeline

GitHub Actions pipelines were used to:

- Build the FastAPI application  
- Validate configuration assumptions  
- Deploy to Azure App Service  

### Pipeline Characteristics

- YAML-based pipelines  
- Separation between CI and deploy stages  
- Deployment gated on CI correctness

### Deployment Failure Handling

Deployment is expected to fail when required cloud infrastructure
or secrets are not present.

This behavior confirms that the pipeline fails explicitly at the
infrastructure boundary rather than masking configuration errors
or reporting false success.

> **Key insight:**  
> CI/CD confirms deployability — not runtime correctness.

Pipeline failures were intentionally encountered when:
- identity configuration was missing  
- environment variables were not defined  
- cloud resources were recreated without re-binding CI/CD  

This reinforced separation between:
- pipeline execution  
- runtime configuration  
- identity management  

---

## Authentication & OIDC (Major Learning)

The most significant learning came from debugging **OIDC authentication failures**.

### Symptoms Observed

- GitHub Actions failed Azure login using OIDC  
- Errors such as `AADSTS700016`  
- App Service workers timing out or being killed  
- Runtime appearing unstable despite successful deployments  

### Root Cause

Identity mismatch between:
- GitHub Actions  
- Azure App Service  
- Application configuration  

### Resolution Approach

- Removed hardcoded identity values  
- Centralized configuration using environment variables  
- Distinguished **bootstrap steps** from automated CI/CD  
- Treated identity as infrastructure, not configuration noise  

> **Key lesson:**  
> Misconfigured authentication can masquerade as infrastructure instability.

---

## Failure Analysis & Debugging

Realistic failures encountered:

- “No instances found” due to quota exhaustion  
- Gunicorn worker timeouts caused by misconfiguration  
- OIDC failures presenting as platform errors  

### Debugging Strategy

- Azure App Service log stream  
- GitHub Actions logs  
- Layer-by-layer isolation:
  - pipeline vs runtime vs identity  

This phase provided the deepest learning in the project.

---

## Database Usage

Azure PostgreSQL Flexible Server was:

- provisioned  
- connected  
- tested during development  

It was later **intentionally deleted** to:
- avoid unnecessary cost  
- demonstrate lifecycle ownership  

The architecture supports external managed databases  
even though none are currently running.

---

## Database Lifecycle

Database schema creation and migration are intentionally treated as  
**bootstrap concerns** and are not executed during application startup.

This avoids implicit infrastructure mutation during deploys or restarts  
and mirrors production-grade operational discipline.

---

## Monitoring & Logging

Primary feedback mechanisms:

- GitHub Actions job logs  
- Azure App Service application logs  

Advanced observability (Application Insights, KQL dashboards) was considered  
architecturally but not deeply implemented, as the focus was on delivery  
systems rather than monitoring tooling depth.

---

## Decommissioning Strategy

All Azure resources were **intentionally deleted** after project completion.

Reasons:
- cost control  
- student subscription limits  
- clean project closure  

The system remains fully reproducible using:
- source control  
- IaC templates  
- documented configuration contracts  

> **Key takeaway:**  
> Designing systems for deletion is as important as designing them for creation.

---

## Key Learnings

- CI/CD success ≠ runtime readiness  
- Infrastructure as Code defines shape, not secrets  
- Identity must be treated as infrastructure  
- Most cloud failures are configuration failures  
- Health checks must validate dependencies  
- Cost awareness is part of engineering responsibility  

---

## Project Status

- 🟢 Learning objectives completed  
- 🟢 Infrastructure reproducible via IaC  
- 🟡 Cloud resources intentionally decommissioned  
- 🟢 Project formally closed  

---

## Purpose

This project exists to demonstrate:

- practical understanding of Azure DevOps concepts  
- real-world CI/CD and authentication failure handling  
- responsible cloud lifecycle management  
- system ownership beyond application code  

The project is intentionally closed after completion.
