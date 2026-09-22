# INF6103 - Cybersécurité des Infrastructures Critiques

Infrastructure as Code (IaC) project for Polytechnique Montréal's critical infrastructure security INF6103 course. This repository contains practical laboratory exercises demonstrating containerization, orchestration, security hardening and penetration testing using modern cloud-native technologies.

## Course Overview

INF6103 focuses on securing critical infrastructure by exploring real-world scenarios involving industrial control systems, containerized applications and Kubernetes orchestration. Students build, deploy, secure, and attack applications in controlled environments to understand security vulnerabilities and mitigation strategies.

## Project Structure

```
inf6103/
├── lab1/
├── lab2/
├── lab3/
├── utils/
│   ├── logger.py
│   ├── resource_creator.py
│   ├── resource_deleter.py
│   └── __init__.py
├── pyproject.toml
├── requirements.txt
└── README.md            # This file
```

## Prerequisites

- Python 3.8+
- AWS account with EC2 access (free tier compatible)
- Git and SSH key pair for AWS

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/ougadicloud/INF6103.git
cd INF6103
```

2. Create Python virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Labs Overview

### Lab 1: Docker & Kubernetes Operations
- Building and managing Docker images
- Deploying applications with Kubernetes
- Image signing and signature verification with Skopeo/GPG
- Understanding Linux capabilities and security

## Utils Module

The `utils/` folder provides shared infrastructure utilities:

- **logger.py** - Centralized logging configuration with INFO level output
- **resource_creator.py** - Boto3-based AWS resource creation (VPC, EC2, security groups, etc.)
- **resource_deleter.py** - Clean resource removal and infrastructure teardown

Each lab can import these utilities to provision and manage AWS infrastructure programmatically.

## Running Labs

Each lab contains its own `main.py` orchestrator:

```bash
cd lab1
python main.py          # Create infrastructure
python main.py delete   # Destroy infrastructure
```

## Authors

**Matricules**: 2051559, 2250224

**Institution**: Polytechnique Montréal

**Semester**: Automne 2026

## License

Academic project - Polytechnique Montréal

## Notes

- All infrastructure is created and destroyed via IaC scripts
- AWS credentials must be configured before running labs
- Free tier restrictions may apply depending on account