# Lab 1: Docker & Kubernetes Operations

This laboratory demonstrates containerization with Docker and orchestration with Kubernetes.

## Objectives

1. Build and manage Docker images
2. Deploy applications using Kubernetes
3. Implement image signing and verification
4. Configure Kubernetes services and deployments

## Infrastructure

- **Instance Type**: m7i-flex.large (2 vCPU, 16 GB RAM)
- **Region**: ca-central-1
- **OS**: Ubuntu 26.04 LTS
- **Container Runtime**: Docker 29.8.0
- **Kubernetes**: Minikube v1.39.0
- **kubectl**: v1.37.0

## Lab Sections

### 1.1 - Docker Operations
- Building the HCC surveillance image
- Comparing container capabilities (--privileged flag)
- Understanding NET_ADMIN capability

### 1.2 - Image Validation & Signatures
- Converting images to OCI format with Skopeo
- Signing manifests with GPG
- Verifying image authenticity and integrity

### 1.3 - Kubernetes Deployment
- Creating Deployments and Services
- Resolving image pull issues
- Deploying the surveillance application to Kubernetes

## Running the Lab

```bash
# Create AWS infrastructure
python main.py

# Delete infrastructure
python main.py delete
```

## Key Commands

### Docker
```bash
docker build -t hcc .
docker run --name hcc-test hcc
docker images
```

### Kubernetes
```bash
minikube start --driver=docker
kubectl create deployment hcc-surveillance --image=hcc
kubectl expose deployment hcc-surveillance --type=NodePort --port=80
minikube service hcc-surveillance
```

### Image Signing
```bash
skopeo copy docker-daemon:hcc:latest oci:./hcc-oci
gpg --detach-sign --armor hcc-oci/index.json
gpg --verify hcc-oci/index.json.asc hcc-oci/index.json
```

## Files

- `main.py` - Infrastructure orchestration script
- `user_data.tpl` - EC2 instance initialization script
- `infra.json` - Generated infrastructure state file

## Authors

Matricules: 2051559, 2250224