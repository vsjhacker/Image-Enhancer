# inference.py

import torch
from torchvision import transforms
from PIL import Image
import mlflow.pytorch
from blur_detection_model import BlurDetectionModel

def process_image(image_path):
    # Load and transform the image
    transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),  # Keep existing augmentations
    transforms.RandomRotation(10),
    transforms.GaussianBlur(kernel_size=5),  # Simulate blur
    transforms.ToTensor(),
    ])
    
    image = Image.open(image_path)
    image = transform(image).unsqueeze(0)

    # Load the model from MLflow
    logged_model = 'runs:/0bf9391ec64a403e91b3d49880c27c4f/blur_detection_model'
    model = mlflow.pytorch.load_model(logged_model)

    # Set the model to evaluation mode
    model.eval()

    # Run inference
    with torch.no_grad():
        output = model(image)
    
    # Process the output
    threshold = 0.6  # You can tune this
    prediction = (output >= threshold).item() # 0 or 1 for blur detection
    if prediction:
        print("The image is blurry.")
    else:
        print("The image is not blurry.")
    
    # Log the result to MLflow
    with mlflow.start_run():
        mlflow.log_param("image_path", image_path)
        mlflow.log_metric("blur_prediction", prediction)

# Example usage
process_image('..//Dataset//Non_Blurry_folder//image_34.jpg')
