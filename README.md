# Backend System – Azure DevOps (AZ-400 Project)

This project was built to gain **hands-on experience with Azure DevOps (AZ-400)** concepts, with a focus on **CI/CD pipelines, Infrastructure as Code (IaC), authentication, and cloud runtime debugging**.

The objective was not application complexity, but understanding **how real delivery systems behave**, how they fail, and how they are responsibly operated and decommissioned.

---

## Project Intent

This project emphasizes:

- CI/CD over feature development
- Infrastructure reproducibility
- Identity and configuration correctness
- Failure analysis and debugging
- Full lifecycle ownership (create → operate → destroy)

The project is intentionally **closed** after achieving learning goals to avoid unnecessary cloud costs.

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

> **Key principle learned:**  
> A successful pipeline deploys artifacts — it does **not** guarantee a healthy runtime.

---

## Repository Structure
<img width="1024" height="559" alt="image" src="https://github.com/user-attachments/assets/71b25e64-7e26-4318-8a98-ba13080d6d09" />

---

## Infrastructure as Code (IaC)

Infrastructure is defined using **Bicep** to ensure reproducibility and controlled provisioning.

### Defined Resources
- App Service Plan (B1)
- Linux App Service (Python runtime)

### IaC File
- infra/appservice.bicep

### Deployment Command
- az deployment group create --resource-group rg-backend-iac --template-file infra/appservice.bicep


Important distinction:
- IaC defines **infrastructure shape**
- Secrets, credentials, and identity are **intentionally excluded**

---

## CI/CD Pipeline

GitHub Actions pipelines were used to:

- Build the FastAPI application
- Package artifacts
- Deploy to Azure App Service

### Pipeline Characteristics
- YAML-based pipelines
- Push-triggered deployments
- Separation between build and deploy stages

> **Key insight:**  
> A green pipeline confirms deployment — not runtime correctness.

Pipeline failures were intentionally allowed when:
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

The architecture supports external managed databases even though none are currently running.

---

## Monitoring & Logging

Primary feedback mechanisms:

- GitHub Actions job logs
- Azure App Service application logs

Advanced observability (Application Insights, KQL dashboards) was considered architecturally but not deeply implemented, as the focus was on delivery systems rather than monitoring tooling depth.

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
- documented configuration steps

> **Key takeaway:**  
> Designing systems for deletion is as important as designing them for creation.

---

## Key Learnings

- CI/CD success ≠ runtime correctness
- Infrastructure as Code defines shape, not secrets
- Identity must be treated as infrastructure
- Many cloud failures are configuration failures
- Debugging across layers is a core DevOps skill
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

The project is intentionally closed after completion.

