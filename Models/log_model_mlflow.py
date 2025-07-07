# log_model_mlflow.py

import mlflow
import torch
import mlflow.pytorch
from blur_detection_model import BlurDetectionModel

def log_model_mlflow():
    model = BlurDetectionModel()
    model.load_state_dict(torch.load("blur_detection_model.pth"))

    # Set up MLflow experiment
    mlflow.set_experiment("Blur Detection Experiment")

    with mlflow.start_run():
        # Log the model
        mlflow.pytorch.log_model(model, "blur_detection_model")

        # Log additional parameters if needed
        mlflow.log_param("model_type", "CNN")
        mlflow.log_param("epochs", 10)
        print("Model logged to MLflow")

if __name__ == "__main__":
    log_model_mlflow()
