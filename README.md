# Image Enhancement Tool

An intelligent image processing application that automatically analyzes and enhances images by optimizing brightness, contrast, saturation, sharpness, and other visual parameters.

![Image Enhancement Tool Screenshot](https://github.com/yourusername/Image-Enchancer/raw/main/app/assets/screenshot.jpg)

## Features

- **Automated Image Analysis**: Analyzes input images to determine current visual parameters
- **Intelligent Enhancement**: Automatically recommends optimal values for:
  - Brightness
  - Contrast
  - Saturation
  - Sharpness
- **Blur Detection**: Automatically detects and reduces blur in images
- **Noise Reduction**: Identifies and removes noise artifacts
- **Real-time Processing**: Shows before/after comparison with visual feedback
- **Download Enhanced Images**: Save your enhanced images directly

## How It Works

1. **Upload an Image**: Select or drag-and-drop an image file (JPG, PNG, JPEG)
2. **Automated Processing**:
   - The app analyzes the image's current metrics
   - Detects blur and noise levels
   - Applies deblurring and denoising if necessary
   - Recommends optimal enhancement values
   - Applies adjustments automatically
3. **Review Results**: Compare the original and enhanced images side by side
4. **Download**: Save the enhanced image to your device

## Technical Details

The tool uses multiple image processing techniques:

- **OpenCV**: For advanced image analysis, blur detection, and noise reduction
- **PIL (Python Imaging Library)**: For image manipulations and enhancements
- **Machine Learning**: Pre-trained models for blur detection
- **Streamlit**: For the interactive web interface

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/Image-Enchancer.git
cd Image-Enchancer

# Install dependencies
pip install -r requirements.txt

# Run the application
cd app
streamlit run main.py
```

## Usage Examples

### Basic Image Enhancement

1. Upload your image using the file uploader
2. Wait for the automatic processing to complete
3. Compare the original and enhanced versions
4. Download the enhanced image using the "Download Enhanced Image" button

### Understanding the Metrics

The tool shows both the current and recommended values for:

- **Saturation**: Controls the intensity of colors (higher values increase color vibrancy)
- **Brightness**: Adjusts how light or dark the image appears
- **Contrast**: Controls the difference between dark and light areas
- **Sharpness**: Enhances the definition of edges and details

## Dataset Storage

For information on how to store large image datasets used with this tool, see the [dataset storage solutions](docs/dataset_storage_solutions.md) documentation.

## Models

The tool uses machine learning models for image analysis. See the [Models README](Models/README.md) for details on how these work.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.