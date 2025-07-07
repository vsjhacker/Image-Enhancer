import streamlit as st
from PIL import Image, ImageEnhance
import numpy as np
from skimage.metrics import mean_squared_error, structural_similarity as ssim
import matplotlib.pyplot as plt
 
# Function to calculate enhancement factors based on histogram analysis
def calculate_enhancement_factors(histogram):
    # Calculate brightness factor based on mean value
    mean_brightness = np.mean(histogram)
    brightness_factor = 1 + (0.5 - mean_brightness / 255) * 0.2  # Subtle adjustment
   
    # Calculate contrast factor based on histogram spread
    contrast_factor = 1 + (np.std(histogram) / 128 - 1) * 0.2  # Subtle adjustment
   
    # Calculate sharpness factor based on edge contrast (approximate using histogram edges)
    sharpness_factor = 1 + (np.mean(histogram[-10:]) - np.mean(histogram[:10])) / 255 * 0.2  # Subtle adjustment
   
    # Calculate saturation factor based on color intensity distribution
    saturation_factor = 1 + (np.percentile(histogram, 95) - np.percentile(histogram, 5)) / 255 * 0.2  # Subtle adjustment
   
    # Ensure factors are within a reasonable range
    brightness_factor = np.clip(brightness_factor, 0.9, 1.1)
    contrast_factor = np.clip(contrast_factor, 0.9, 1.3)
    sharpness_factor = np.clip(sharpness_factor, 0.9, 1.1)
    saturation_factor = np.clip(saturation_factor, 0.9, 1.3)

    print("Brightness value: ", brightness_factor)
    print("Contrast value: ", contrast_factor)
    print("Sharpness value :", sharpness_factor)
    print("Saturation value: ", saturation_factor)
    print("="*10)
 
    return brightness_factor, contrast_factor, sharpness_factor, saturation_factor
 
# Streamlit app
st.title("Subtle Image Enhancement Based on Image Statistics")
 
# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
 
if uploaded_file is not None:
    # Load the image
    image = Image.open(uploaded_file)
 
    # Convert to grayscale for histogram analysis
    grayscale_image = image.convert("L")
    histogram = np.array(grayscale_image.histogram())
 
    # Calculate enhancement factors
    brightness_factor, contrast_factor, sharpness_factor, saturation_factor = calculate_enhancement_factors(histogram)
 
    # Apply enhancements based on calculated values
    enhancer = ImageEnhance.Brightness(image)
    enhanced_image = enhancer.enhance(brightness_factor)
 
    enhancer = ImageEnhance.Contrast(enhanced_image)
    enhanced_image = enhancer.enhance(contrast_factor)
 
    enhancer = ImageEnhance.Sharpness(enhanced_image)
    enhanced_image = enhancer.enhance(sharpness_factor)
 
    enhancer = ImageEnhance.Color(enhanced_image)
    enhanced_image = enhancer.enhance(saturation_factor)

    oringinal_img = np.array(image)
    enh_img = np.array(enhanced_image)
    # Calculate Mean Squared Error (MSE)
    mse_value = mean_squared_error(oringinal_img, enh_img)

    # Convert both images to numpy arrays for histogram comparison
    original_array = np.array(image)
    enhanced_array = np.array(enhanced_image)
    
    # Histogram Comparison
    plt.figure(figsize=(10, 6))
    plt.hist(original_array.flatten(), bins=256, color='blue', alpha=0.5, label='Original')
    plt.hist(enhanced_array.flatten(), bins=256, color='red', alpha=0.5, label='Enhanced')
    plt.title('Histogram Comparison')
    plt.legend()
    st.pyplot(plt)
 
    # # Calculate Structural Similarity Index (SSIM)
    # ssim_value, _ = ssim(oringinal_img, enh_img, full=True, multichannel=True)

    print("Mean squared error: ", mse_value)
    # print("ssim_value : ",ssim_value)
 
    # Display original and enhanced images side by side
    col1, col2 = st.columns(2)
    with col1:
        st.image(image, caption="Original Image", use_column_width=True)
    with col2:
        st.image(enhanced_image, caption="Enhanced Image", use_column_width=True)
 
    # Option to download the enhanced image
    output_path = "enhanced_image.jpg"
    enhanced_image.save(output_path)
    with open(output_path, "rb") as file:
        st.download_button(label="Download Enhanced Image", data=file, file_name=output_path, mime="image/jpeg")