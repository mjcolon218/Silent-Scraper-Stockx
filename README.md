# Sneaker Price Tracker (Silent Scalper)

## 🧠 Overview
Silent Scalper is a serverless sneaker price tracker that scrapes StockX for sneaker listings based on search terms, extracts prices and images, and alerts you when a price drops below your target. It includes a CLI interface, a Lambda backend, DynamoDB storage, and CI/CD via GitHub Actions and ECR.

---

## 🔧 Features
- 📦 Containerized Python scraper using Playwright & BeautifulSoup
- 🔍 Search sneakers by keyword
- 💵 Track lowest price & image
- 📊 Store and update target price in DynamoDB
- ⚙️ AWS Lambda backend (via Docker image)
- 📜 CI/CD pipeline: test, build, push to ECR, deploy to Lambda
- 🖥️ CLI commands for managing tracked sneakers
- 🔒 GitHub secrets for secure deployments

---

## 📁 Project Structure
```bash
├── Dockerfile
├── requirements.txt
├── stockx_api.py          # Core scraper logic
├── add_sneaker.py         # CLI to add new sneaker
├── update_target.py       # CLI to update target price
├── list_sneakers.py       # CLI to list all sneakers
├── test_runner.py         # Run all unit tests
├── tests/                 # Unit test files
└── .github/workflows/ci.yml
```

---

## 📦 Prerequisites
- AWS CLI configured with IAM user (Programmatic access)
- IAM permissions:
  - ECR: `ecr:*`
  - Lambda: `lambda:UpdateFunctionCode`
  - DynamoDB: `dynamodb:PutItem`, `GetItem`, `Scan`, `UpdateItem`
- Docker installed locally
- Python 3.11 environment
- GitHub secrets configured:
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `AWS_ACCOUNT_ID`
  - `ECR_REPO_NAME` (e.g., `silent-scalper`)
  - `AWS_REGION`

---

## 🚀 AWS Services Used
- **Amazon ECR** – Store Docker images
- **AWS Lambda (container image)** – Run the scraper on demand
- **Amazon DynamoDB** – Store sneaker and price metadata
- **Amazon CloudWatch** – Log Lambda invocations
- **GitHub Actions** – CI/CD for tests + deploy

🖼️ *Image links below will be added once screenshots are uploaded:*
- ECR Console → `![ECR Repo](images/ecr.png)`
- Lambda Console → `![Lambda Setup](images/lambda.png)`
- CloudWatch Logs → `![CloudWatch Logs](images/logs.png)`
- DynamoDB Table → `![DynamoDB Table](images/dynamodb.png)`

---

## 🛠️ Setup & CLI Usage

### 1️⃣ Add a Sneaker
```bash
python add_sneaker.py "jordan 4" 220
```

### 2️⃣ List All Tracked Sneakers
```bash
python list_sneakers.py
```

### 3️⃣ Update a Target Price
```bash
python update_target.py "jordan 4" 210
```

---

## 🧪 Run Unit Tests
```bash
python test_runner.py
```

---

## 🐳 Docker Commands
```bash
# Build
docker build -t silent-scalper .

# Run locally
docker run --rm silent-scalper
```

---

## 🔁 CI/CD Workflow Highlights
- Push to `main` →
  - ✅ Run tests
  - 🛠 Build Docker image
  - ☁️ Push to ECR
  - 🚀 Update Lambda image

---

## 🧼 Clean-Up (Optional)
To remove resources:
- `aws ecr delete-repository --repository-name silent-scalper --force`
- Delete Lambda via console or `aws lambda delete-function`
- Delete DynamoDB table manually

---

## 🧠 Future Additions
- Email/SMS notifications
- Athena + CloudWatch Log queries
- Step Functions for retries
- Dashboard for visual tracking

---

Ready to deploy consulting-grade sneaker tracking apps. 🔥

---
