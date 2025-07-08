import streamlit as st
from PIL import Image, ImageEnhance
import numpy as np
import yaml
import sys
import traceback

# Try to import OpenCV, but provide a fallback if it's not available
try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
    st.warning("OpenCV (cv2) is not available. Some image processing features will be limited.")

# Import helper functions with error handling
try:
    from utility.helper import get_image_metrics, detect_blur, detect_noise, remove_blur, remove_noise, recommend_value, apply_adjustments
except ImportError as e:
    st.error(f"Error importing helper functions: {e}")
    traceback.print_exc()
    
    # Define fallback functions if imports fail
    def get_image_metrics(image):
        return 1.0, 1.0, 1.0, 1.0  # Default values
        
    def recommend_value(current, low_threshold, high_threshold):
        return current  # Return same value
        
    def apply_adjustments(image, sat, bright, cont, sharp):
        return image  # Return original image
    
    # These functions need OpenCV, so they'll be limited without it
    def detect_blur(image_np):
        return 200  # Default value (not blurry)
        
    def detect_noise(image_np):
        return 0  # Default value (no noise)
        
    def remove_blur(image_np):
        return image_np  # Return original image
        
    def remove_noise(image_np):
        return image_np  # Return original image

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
        if OPENCV_AVAILABLE:
            try:
                noise_level = detect_noise(image_np)
                blur_level = detect_blur(image_np)
            except Exception as e:
                st.warning(f"Error in image analysis: {e}")
                noise_level = 0
                blur_level = 200  # Default values
        else:
            st.info("OpenCV is not available. Skipping image analysis steps.")
            noise_level = 0
            blur_level = 200  # Default values

        # Step 3: Apply denoising and deblurring if necessary
        if OPENCV_AVAILABLE:
            if noise_level > 10:
                image_np = remove_noise(image_np)
            if blur_level < 100:
                image_np = remove_blur(image_np)
        else:
            st.info("OpenCV is not available. Skipping denoising and deblurring steps.")

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
            st.image(image_01, use_container_width=True)

        with col2:
            st.subheader("Adjusted Image")
            st.image(adjusted_image, use_container_width=True)

        # Print current and recommended values
        st.write(f"Current Saturation: {saturation_value:.2f}")
        st.write(f"Current Brightness: {brightness_value:.2f}")
        st.write(f"Current Contrast: {contrast_value:.2f}")
        st.write(f"Current Sharpness: {sharpness_value:.2f}")
        st.write(f"Recommended Saturation: {recommended_saturation:.2f}")
        st.write(f"Recommended Brightness: {recommended_brightness:.2f}")
        st.write(f"Recommended Contrast: {recommended_contrast:.2f}")
        st.write(f"Recommended Sharpness: {recommended_sharpness:.2f}")
        
        # Add download button for the adjusted image
        import io
        import os
        import datetime
        
        # Create download section
        st.subheader("Download Options")
        
        # Prepare image for download
        buf = io.BytesIO()
        adjusted_image.save(buf, format="JPEG")
        byte_im = buf.getvalue()
        
        # Create two columns for download buttons
        dl_col1, dl_col2 = st.columns(2)
        
        with dl_col1:
            st.download_button(
                label="Download Enhanced Image",
                data=byte_im,
                file_name="enhanced_image.jpg",
                mime="image/jpeg",
                help="Download the enhanced version of your image"
            )
            
        # Create metadata file with enhancement information
        try:
            metadata_path = os.path.join(os.path.dirname(__file__), "image_enhancement_info.txt")
            if os.path.exists(metadata_path):
                with open(metadata_path, "r") as f:
                    info_content = f.read()
                
                # Get current date and time
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Add specific image metrics to the info
                image_specific_info = f"""
                
Original Image Metrics:
- Saturation: {saturation_value:.2f}
- Brightness: {brightness_value:.2f}
- Contrast: {contrast_value:.2f}
- Sharpness: {sharpness_value:.2f}

Applied Enhancements:
- Saturation: {recommended_saturation:.2f}
- Brightness: {recommended_brightness:.2f}
- Contrast: {recommended_contrast:.2f}
- Sharpness: {recommended_sharpness:.2f}

Blur Level: {blur_level:.2f}
Noise Level: {noise_level:.2f}

Date Processed: {current_time}
                """
                
                complete_info = info_content + image_specific_info
                
                with dl_col2:
                    st.download_button(
                        label="Download Enhancement Info",
                        data=complete_info,
                        file_name="image_enhancement_details.txt",
                        mime="text/plain",
                        help="Download details about the enhancements applied"
                    )
        except Exception as e:
            st.warning(f"Could not generate enhancement info: {e}")
            
        # Option to save the enhanced image locally
        st.write("---")
        if st.button("Save to local OutputImages folder"):
            try:
                output_dir = "../OutputImages"
                os.makedirs(output_dir, exist_ok=True)
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                save_path = os.path.join(output_dir, f"enhanced_{timestamp}.jpg")
                adjusted_image.save(save_path)
                st.success(f"Image saved to {save_path}")
            except Exception as e:
                st.error(f"Failed to save image: {e}")
