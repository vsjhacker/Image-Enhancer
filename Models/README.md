# Models Directory Documentation

This directory contains the machine learning components of the Image Enhancement Tool. These models, particularly the blur detection model, play a crucial role in the automated image enhancement process.

## Overview

The models in this directory enable the application to:

1. Detect whether an image is blurry
2. Make intelligent decisions about which enhancements to apply
3. Track model versions and performance

## Files and Their Purpose

### 1. `blur_detection_model.py`

**Purpose**: Defines the neural network architecture for blur detection.

**Key components**:
- `BlurDetectionModel` class: A PyTorch CNN with:
  - Three convolutional layers with batch normalization
  - Max pooling layers
  - Dropout for regularization (0.5)
  - Fully connected layers
  - Sigmoid output for binary classification (blurry vs. non-blurry)
- `save_model()` function: Initializes and saves the model

**Architecture details**:
```
Input Image → Conv1 (3→32) → ReLU → MaxPool → 
             Conv2 (32→64) → ReLU → MaxPool → 
             Conv3 (64→128) → ReLU → MaxPool → 
             Flatten → Dropout → FC1 (128*28*28→128) → FC2 (128→1) → Sigmoid
```

### 2. `blur_detection_model.pth`

**Purpose**: Contains the trained weights and parameters of the blur detection model.

**Usage**:
- Loaded during inference
- Eliminates the need for retraining
- Ensures consistent performance

### 3. `inference.py`

**Purpose**: Provides functionality to use the trained model on new images.

**Key features**:
- Image preprocessing pipeline:
  - Resizing to 224×224
  - Data augmentation (horizontal flip, rotation)
  - Conversion to tensor format
- Model loading from MLflow
- Inference with configurable threshold (currently 0.6)
- Result logging to MLflow

**Usage example**:
```python
process_image('path/to/image.jpg')
```

### 4. `log_model_mlflow.py`

**Purpose**: Manages model versioning and experiment tracking using MLflow.

**Functionality**:
- Logs the trained model to MLflow
- Tracks experiment parameters
- Creates versioned model artifacts
- Facilitates model deployment

## Integration with the Main Application

These models are integrated with the main application (`app/main.py`) to:

1. Analyze uploaded images
2. Detect blur levels
3. Apply appropriate enhancements based on image characteristics
4. Improve image quality automatically

## MLflow Integration

The project uses MLflow for:

1. **Experiment Tracking**: Recording parameters, metrics, and artifacts
2. **Model Registry**: Managing model versions
3. **Model Serving**: Loading models for inference
4. **Reproducibility**: Ensuring consistent results

## How to Use

To use these models directly:

1. For blur detection on a single image:
   ```
   cd Models
   python inference.py  # Edit the file to change the target image
   ```

2. To log a new model version to MLflow:
   ```
   cd Models
   python log_model_mlflow.py
   ```

3. To train a new model (requires setting up a training script):
   ```
   # Training script would be needed
   ```

## Future Improvements

Potential enhancements for the models:

1. Add more specialized models for other image quality issues (noise, contrast, etc.)
2. Implement model quantization for faster inference
3. Add explainability features to visualize which parts of images are detected as blurry
4. Expand the training dataset for improved accuracy
5. Implement ensemble methods for more robust predictions

## Dependencies

- PyTorch
- torchvision
- MLflow
- PIL (Pillow)
