import streamlit as st
from PIL import Image, ImageEnhance
import numpy as np
import cv2
import yaml
from utility.helper import get_image_metrics, detect_blur, detect_noise, remove_blur, remove_noise, recommend_value, apply_adjustments

def load_thresholds(file_path):
    # function to load the yaml configurationm file
    with open(file_path, 'r') as file:
        thresholds = yaml.safe_load(file)
    return thresholds

# Load thresholds from the YAML file
thresholds = load_thresholds('./config/thersholds.yaml')

# Extract the values
saturation_low_threshold = thresholds['saturation']['low_threshold']
saturation_high_threshold = thresholds['saturation']['high_threshold']
brightness_low_threshold = thresholds['brightness']['low_threshold']
brightness_high_threshold = thresholds['brightness']['high_threshold']
contrast_low_threshold = thresholds['contrast']['low_threshold']
contrast_high_threshold = thresholds['contrast']['high_threshold']
sharpness_low_threshold = thresholds['sharpness']['low_threshold']
sharpness_high_threshold = thresholds['sharpness']['high_threshold']

# Streamlit app
st.title('Image Enhancement Tool')

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    st.write("Processing the image, please wait...")

    # Initialize progress bar
    progress_bar = st.progress(0.0)
    
    # Simulate processing steps
    steps = 4  # Total number of steps in processing
    step_size = 1.0 / steps
    
    with st.spinner('Processing...'):
        # Load the image
        image_01 = Image.open(uploaded_file)
        image_np = np.array(image_01)
        
        # Step 1: Get current metrics
        progress_bar.progress(step_size)
        saturation_value, brightness_value, contrast_value, sharpness_value = get_image_metrics(image_01)
        
        # Step 2: Detect noise and blur
        progress_bar.progress(2 * step_size)
        noise_level = detect_noise(image_np)
        blur_level = detect_blur(image_np)

        # Step 3: Apply denoising and deblurring if necessary
        if noise_level > 10:
            image_np = remove_noise(image_np)
        if blur_level < 100:
            image_np = remove_blur(image_np)

        # Step 4: Convert back to PIL image
        image = Image.fromarray(image_np)

        # Step 5: Recommend values
        progress_bar.progress(3 * step_size)
        recommended_saturation = recommend_value(saturation_value, saturation_low_threshold, saturation_high_threshold)
        recommended_brightness = recommend_value(brightness_value, brightness_low_threshold, brightness_high_threshold)
        recommended_contrast = recommend_value(contrast_value, contrast_low_threshold, contrast_high_threshold)
        recommended_sharpness = recommend_value(sharpness_value, sharpness_low_threshold, sharpness_high_threshold)

        # Step 6: Apply adjustments
        adjusted_image = apply_adjustments(image, recommended_saturation, recommended_brightness, recommended_contrast, recommended_sharpness)

        # Update progress bar to 100%
        progress_bar.progress(1.0)

        # Display results side by side
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Original Image")
            st.image(image_01, use_column_width=True)

        with col2:
            st.subheader("Adjusted Image")
            st.image(adjusted_image, use_column_width=True)

        # Print current and recommended values
        st.write(f"Current Saturation: {saturation_value:.2f}")
        st.write(f"Current Brightness: {brightness_value:.2f}")
        st.write(f"Current Contrast: {contrast_value:.2f}")
        st.write(f"Current Sharpness: {sharpness_value:.2f}")
        st.write(f"Recommended Saturation: {recommended_saturation:.2f}")
        st.write(f"Recommended Brightness: {recommended_brightness:.2f}")
        st.write(f"Recommended Contrast: {recommended_contrast:.2f}")
        st.write(f"Recommended Sharpness: {recommended_sharpness:.2f}")
