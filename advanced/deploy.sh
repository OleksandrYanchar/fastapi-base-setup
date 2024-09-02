#!/bin/bash

# Set the namespace
NAMESPACE="fastapi-namespace"

# Apply the namespace
kubectl apply -f k8s/namespace.yaml

# Apply ConfigMap
kubectl apply -f k8s/configmap.yaml

# Apply Secret
kubectl apply -f k8s/secret.yaml

# Deploy PostgreSQL
kubectl apply -f k8s/postgres/

# Deploy FastAPI backend
kubectl apply -f k8s/backend/

# Deploy Nginx
kubectl apply -f k8s/nginx/

# Deploy Adminer (optional)
kubectl apply -f k8s/adminer/

# Confirm deployments and services
kubectl get deployments -n $NAMESPACE
kubectl get services -n $NAMESPACE

echo "Starting port forwarding..."
kubectl port-forward service/nginx 8000:80 -n $NAMESPACE &
kubectl port-forward service/adminer 5051:5051 -n $NAMESPACE &

echo "Deployment complete! Access FastAPI at http://localhost:8000 and Adminer at http://localhost:5051"
