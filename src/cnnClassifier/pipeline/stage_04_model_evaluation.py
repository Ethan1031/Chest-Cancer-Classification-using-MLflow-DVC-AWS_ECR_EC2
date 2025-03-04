import os
import tensorflow as tf
from cnnClassifier.config.configuration import ConfigurationManager
from cnnClassifier.components.model_evaluation_mlflow import Evaluation
from cnnClassifier import logger

STAGE_NAME = "Evaluation stage"

class EvaluationPipeline:
    def __init__(self):
        pass
        
    def main(self):
        # Set MLflow environment variables
        os.environ["MLFLOW_TRACKING_URI"] = "https://dagshub.com/Ethan1031/End-to-End-Project-Using-MLflow-DVC-with-CICD-Deployment.mlflow"
        os.environ["MLFLOW_TRACKING_USERNAME"] = "Ethan1031"
        os.environ["MLFLOW_TRACKING_PASSWORD"] = "d37862c13aa955d1ee548654d6d5323c48adbe4b"
        
        try:
            # Fix GPU memory issues if needed
            gpus = tf.config.experimental.list_physical_devices('GPU')
            if gpus:
                for gpu in gpus:
                    tf.config.experimental.set_memory_growth(gpu, True)
            
            config = ConfigurationManager()
            eval_config = config.get_evaluation_config()
            evaluation = Evaluation(eval_config)
            
            logger.info(f">>> Starting {STAGE_NAME} <<<")
            evaluation.evaluation()
            evaluation.log_into_mlflow()
            logger.info(f">>> Completed {STAGE_NAME} <<<")
            
        except Exception as e:
            logger.error(f"Error in {STAGE_NAME}: {e}")
            raise e


if __name__ == '__main__':
    try:
        logger.info(f"*******************")
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = EvaluationPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
            