from PIL import Image, ImageEnhance
import numpy as np
import cv2

def get_image_metrics(image):
    """
        get_image_metrics: Extract the brightness, saturation, contrast
                        and sharpness of the image
                
        Params:
            - image: image loads in PIL or opencv

        returns:
            - average saturation, average brightness, average contrast and
            average sharpness value.
    """
    image_np = np.array(image)
    image_hsv = cv2.cvtColor(image_np, cv2.COLOR_RGB2HSV)
    hsv_saturation = image_hsv[:, :, 1]
    hsv_brightness = image_hsv[:, :, 2]
    avg_saturation = np.mean(hsv_saturation)
    avg_brightness = np.mean(hsv_brightness)
    image_gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
    contrast = np.std(image_gray)

    def compute_sharpness(img):
        """
            compute sharpness of the image
        """
        laplacian = cv2.Laplacian(img, cv2.CV_64F)
        sharpness = np.var(laplacian)
        return sharpness
    
    sharpness = compute_sharpness(image_np)
    
    return avg_saturation, avg_brightness, contrast, sharpness

def detect_noise(image_np):
    """
        detect_noise: detect the image contains
                    noise or not

        Params:
            - image_np: Numpy array of the image

        return:
            - Noise level of the image
    """
    noise_level = np.std(image_np)
    return noise_level

def detect_blur(image_np):
    """
        detect_blur: detect the image contains
                blur or not

        Params:
            - image_np: Numpy array of the image

        return:
            - Blurness of the image
    """
    laplacian = cv2.Laplacian(image_np, cv2.CV_64F)
    variance = laplacian.var()
    return variance

def remove_noise(image_np):
    # remove noise from the image
    return cv2.fastNlMeansDenoisingColored(image_np, None, h=10, hColor=10, templateWindowSize=7, searchWindowSize=21)

def remove_blur(image_np):
    # remove blur from the image
    kernel = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])
    return cv2.filter2D(image_np, -1, kernel)

def apply_adjustments(image, saturation_value, brightness_value, contrast_value, sharpness_value):
    """
        apply_adjustments: it will apply the enhancements to the image.

        Params:
            - image: Image need the enhancement
            - saturation_value: recommended value
            - brightness_value: recommended value
            - contrast_value: recommended value
            - sharpness_value: recommended value

        returns:
            - return the enhanced image
    """
    enhancer = ImageEnhance.Color(image)
    saturation_factor = 1.0 + (saturation_value - 5) * 0.2
    saturation_factor = max(1.0, min(2.0, saturation_factor))
    image = enhancer.enhance(saturation_factor)

    enhancer = ImageEnhance.Brightness(image)
    brightness_factor = 1.0 + (brightness_value - 5) * 0.2
    brightness_factor = max(1.0, min(2.0, brightness_factor))
    image = enhancer.enhance(brightness_factor)
    
    enhancer = ImageEnhance.Contrast(image)
    contrast_factor = 1.0 + (contrast_value - 5) * 0.2
    contrast_factor = max(1.0, min(2.0, contrast_factor))
    image = enhancer.enhance(contrast_factor)
    
    image_np = np.array(image)
    
    def apply_sharpness(img, alpha):
        # apply the sharpness to the image
        alpha = max(0.0, min(2.0, alpha))
        kernel = np.array([[-1, -1, -1], [-1, 9 + alpha, -1], [-1, -1, -1]])
        return cv2.filter2D(img, -1, kernel)

    image_np = apply_sharpness(image_np, (sharpness_value - 5) * 0.2)
    image = Image.fromarray(image_np)

    return image

def recommend_value(current_value, low_threshold, high_threshold):
    """
        recommend_value: it will recommend the values for the metrics.

        Params:
            - cuurent_value: current particular metric value
            - low_thershold: min value of the metric
            - high_thershold: max value of the metric

        returns:
            - recommended enhanced value for the particualr metric.
    """
    if current_value < low_threshold:
        return min(10, (current_value / low_threshold) * 10)
    elif current_value > high_threshold:
        return max(0, 10 - ((current_value - high_threshold) / (255 - high_threshold)) * 10)
    else:
        return 5
    
