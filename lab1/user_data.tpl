#!/bin/bash

echo "=========================================="
echo "Setting up EC2 instance for INF6103 Lab"
echo "=========================================="

apt-get update
apt-get upgrade -y

echo "Installing basic tools..."
apt-get install -y curl wget git vim nano openssh-server openssh-client

echo "Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
usermod -aG docker ubuntu
rm get-docker.sh

echo "Installing Minikube..."
curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-amd64
install minikube-linux-amd64 /usr/local/bin/minikube
rm minikube-linux-amd64

echo "Installing kubectl..."
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
rm kubectl

echo "Installing Skopeo and GnuPG..."
apt-get install -y skopeo gnupg

echo "Starting Minikube..."
sudo -u ubuntu minikube start --driver=docker --cpus=3 --memory=4096 --disk-size=20gb

echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
docker --version
kubectl version --client --short
sudo -u ubuntu minikube status
echo "2051559, 2250224" && date
echo "=========================================="