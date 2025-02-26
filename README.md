# End-to-End-Project-Using-MLflow-DVC-with-CICD-Deployment

Experiments code:
import dagshub
dagshub.init(repo_owner='Ethan1031', repo_name='End-to-End-Project-Using-MLflow-DVC-with-CICD-Deployment', mlflow=True)

import mlflow
with mlflow.start_run():
mlflow.log_param('parameter name', 'value')
mlflow.log_metric('metric name', 1)
