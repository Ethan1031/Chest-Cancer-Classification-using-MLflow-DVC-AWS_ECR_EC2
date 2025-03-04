# End-to-End-Project-Using-MLflow-DVC-with-CICD-Deployment

## Overview
This project demonstrates an end-to-end machine learning workflow using MLflow and DVC with CI/CD deployment to AWS. The application uses transfer learning with VGG16 for image classification.

## Setup

### Environment
```bash
source "mlflow project/bin/activate"
```

### MLflow Integration
```python
import dagshub
dagshub.init(repo_owner='Ethan1031', repo_name='End-to-End-Project-Using-MLflow-DVC-with-CICD-Deployment', mlflow=True)
```

## Workflow Stages

### Stage 1: Data Ingestion
- Loads configuration files (config.yaml, params.yaml) containing setup parameters
- Creates necessary directories (artifacts/data_ingestion) for storing raw data
- Fetches data from data source and saves the dataset in the created directories

### Stage 2: Base Model Preparation
- Loads configuration values from config.yaml and params.yaml (defines hyperparameters and paths)
- Prepares the base model using Pretrained VGG16 architecture
- Modifies the model:
  - Freezes all layers for transfer learning
  - Adds a Flatten layer to convert features into a vector
  - Adds a Dense layer for classification
- Compiles using SGD optimizer with the provided learning rate
- Saves the model to .keras or .h5 file

### Stage 3: Model Training
- Loads training configuration from config.yaml and params.yaml
- Loads the updated base model from the previous step
- Compiles the model:
  - Configures Adam optimizer (instead of SGD)
  - Uses binary cross-entropy loss function for two-class problem
  - Sets appropriate metrics
- Creates data generator for training and validation:
  - 68 images for training and 275 images for validation
  - Rescales images to [0,1] range
  - Splits dataset: 80% training, 20% validation
  - Uses data augmentation if enabled
  - Loads images from the dataset directory
- Trains the model for specified epochs using Keras fit()
- Logs accuracy (0.6400 initially) and loss
- Saves the final trained model for deployment
- Tracks the model using DVC

#### DVC Usage
DVC (Data Version Control) manages:
- Raw dataset versions for storing and rolling back
- Transformed or processed datasets
- Model checkpoints for different versions of trained models
- Training logs: metrics, loss values, and parameters

DVC commands:
```bash
# Initialize DVC directory
dvc init

# Run all predefined steps (skips unchanged files)
dvc repro

# Check dependencies between files
dvc dag

# Commit changes & push to remote storage
dvc push

# Pull previous versions
dvc pull
```

### Stage 4: Model Evaluation
- Sets up MLflow tracking:
  - Connects to external MLflow server hosted on DagsHub
  - Uses environment variables for authentication
- Loads the trained model (model.h5) for evaluation
- Defines configuration class to store evaluation settings
- Evaluates model on test data:
  - Makes predictions
  - Computes accuracy
  - Generates classification report
- Logs evaluation metrics to MLflow:
  - Batch size, accuracy, loss, confusion matrix
  - Saves model to MLflow artifacts
- Registers model in MLflow:
  - Creates different experiments for multiple model versions
  - Moves best performing models from staging to production

### Stage 5: AWS Deployment
Implements end-to-end CI/CD of MLflow project to AWS using GitHub Actions:

#### AWS Setup
- Creates AWS IAM User with permissions:
  - AmazonEC2FullAccess (for managing EC2 instances)
  - AmazonEC2ContainerRegistryFullAccess (for ECR access)
- Saves AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY

#### Dockerize MLflow
- Creates AWS ECR Repository (private container registry)
- Builds and pushes Docker image of MLflow project

#### EC2 Deployment
- Creates and launches EC2 instance to host MLflow model
- Records public IP address
- Installs Docker & AWS CLI on EC2
- Connects via SSH
- Pulls image and runs container
- Sets up self-hosted GitHub Actions Runner on EC2


CI/CD with GitHub Actions - Automates Build & Deployment
Setting Up CI/CD with GitHub Actions
Configure GitHub Secrets
Configure GitHub Actions by creating .github/workflows/deploy.yaml to automating Deployment & Running MLflow on EC2

