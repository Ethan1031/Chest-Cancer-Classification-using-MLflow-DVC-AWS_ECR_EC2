# End-to-End-Project-Using-MLflow-DVC-with-CICD-Deployment

Experiments code:
import dagshub
dagshub.init(repo_owner='Ethan1031', repo_name='End-to-End-Project-Using-MLflow-DVC-with-CICD-Deployment', mlflow=True)


# Environment

source "mlflow project/bin/activate"

Stage by stage Workflows: 
Stage 1: Data Ingestion
Loads Configuration Files (config.yaml, params.yaml). These files contain setup parameters for datasets, paths, and model hyperparameters.
Creates Necessary Directories (artifacts/data_ingestion) for storing raw data for further processing.
Fetching data from data source and saving the dataset at directories we created last step. 

Stage 2: Base Model Preparation Workflows: 
Load configuration values from config.yaml and params.yaml. (define hyperparameters and path).
Prepare the base model by defining its architecture using the Pretrained Model (VGG16) and load pretrained weights (imagenet or custom).
Modify the Model by:
Freezes all layers (transfer learning) to retain pretrained knowledge.
Adds a Flatten layer to convert features into a vector.
Adds a Dense layer for classification.

Compile by using SGD optimizer with the provided learning rate.
Save the model to .keras or .h5 file. 

Stage 3: Model Training
Loads training configuration values from config.yaml and params.yaml.
Loads the updated base model from the previous step.
Compile the model by:
Configures optimizer (Uses Adam optimizer instead of SGD)
Loss function (Uses binary cross-entropy since it’s a two-class problem) and metrics.

Creates data generator for training and validation: 
68 images for training and 275 images for validation.
Rescales images to [0,1] range.
Splits dataset into 80% training, 20% validation.
Uses data augmentation if enabled.
Loads images from the dataset directory.
Trains the model for N epochs, batch training and validates on validation set. 

Uses Keras fit() function to train the model.
Logs accuracy (0.6400 initially) and loss.
Saves the final trained model to be used in deployment.

Track the model using DVC. 
DVC (Data Version Control) for Version Tracking:
Raw dataset versions for storing and rolling back.
Keeps track of transformed or processed datasets.
Model Checkpoints which store different versions of trained models.
Training Logs: Tracks metrics, loss values, and parameters.

We can run DVC in two ways: on your data, on your pipeline. 
How Does DVC Work?
Initialize DVC directory: dvc init
Running all predefined steps: dvc repro, if the file is running before and no updating, it will skip running this file, which allows us no need to run all the things from scratch. 
Check the dependencies between each running file: dvc dag
Commit Changes & Push to Remote Storage: dvc push 
Pull Previous Versions Anytime: dvc pull


Stage 4: Model Evaluation Workflow (Including Experiment Tracking and Model Registration from staging to production)
MLflow Tracking Setup
Connecting to an external MLflow server hosted on DagsHub.
Uses environment variables for authentication.

Loading the Trained Model as model.h5 for evaluation. 
Define Configuration Class
Define Evaluation Configuration Class to store evaluation settings like model path, dataset path, batch size, and MLflow URI.
Evaluate Model on Test Data. 
Make predictions, compute accuracy and generate a classification report.

Log Evaluation Metrics to MLflow
Log Metrics & Artifacts to MLflow (batch size, accuracy, loss, confusion matrix).
Saves model to MLflow artifacts.

Register Model in MLflow
Creates different experiments to get multiple model versions.
Move the best performing models from staging to production.


Stage 5: Model Deployment on AWS
End-to-end CICD of an MLflow project to AWS production environment using GitHub Actions
Using AWS services to deploy an MLflow project with a structured CI/CD pipeline using GitHub Actions. 

AWS Setup (IAM User, ECR, EC2)
Create an AWS IAM User for deployment
Setting up permissions for managing AWS resources via GitHub Actions:
AmazonEC2FullAccess (for managing EC2 instances)
AmazonEC2ContainerRegistryFullAccess (for ECR access)
Save AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY for later use.

Dockerize MLflow - Build & Push Image to ECR
Creating AWS Resources: ECR (Elastic Container Registry) & EC2 Instance
Create ECR Repository (A private AWS container registry where we will push our Docker image): Building and Pushing Docker Image of MLflow Project

Deploy on EC2 - Pull Image, Run Container
Install Docker & AWS CLI on EC2
Once the EC2 instance is running, install Docker to run our MLflow container.
Connect to EC2 via SSH
Pull the Image and run the container

Create an EC2 Instance and Launch Instance (Used to host our MLflow model): Deploying the MLflow Model in AWS (EC2)
Launch and note down Public IP Address of EC2.
Setting up a Self-Hosted GitHub Actions Runner on EC2


CI/CD with GitHub Actions - Automates Build & Deployment
Setting Up CI/CD with GitHub Actions
Configure GitHub Secrets
Configure GitHub Actions by creating .github/workflows/deploy.yaml to automating Deployment & Running MLflow on EC2

