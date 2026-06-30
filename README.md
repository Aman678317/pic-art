# Pic-Art: Image Color Analysis Prototype

This is a barebones prototype built for the Product Management Internship Assignment. It analyzes images at the pixel level and provides a percentage breakdown of the 11 primary colors present in the image.

## 11 Color Categories Supported
The colors in the image are mapped to one of the following 11 categories using perceptual color distance (CIELAB color space):

| Category | Hex Color |
| -------- | --------- |
| White    | `#FFFFFF` |
| Black    | `#000000` |
| Red      | `#FF0000` |
| Green    | `#00A651` |
| Yellow   | `#FFD700` |
| Blue     | `#0066FF` |
| Brown    | `#8B4513` |
| Purple   | `#800080` |
| Pink     | `#FF69B4` |
| Orange   | `#FF8C00` |
| Gray     | `#808080` |

## Setup Instructions
To run this prototype locally, you will need Python installed on your machine.

1. Clone this repository or download the source code.
2. Install the required dependencies using pip:
   ```bash
   pip install pillow scikit-image matplotlib numpy
   ```

## Usage

1. Place your target images (`.jpg`, `.jpeg`, `.png`) in the same directory as the script.
2. Run the script:
   ```bash
   python prototype.py
   ```
3. The script will automatically detect the images, process them, and generate new image files (e.g., `chart_image.png`) that show the original image side-by-side with the precise color percentage pie chart.

Alternatively, you can pass specific image paths as arguments:
```bash
python prototype.py path/to/your/image.jpg
```

## Features
- **Accurate Color Mapping:** Converts RGB to LAB color space to calculate Delta E (perceptual distance), ensuring colors like navy map to Blue, burgundy to Red, etc.
- **Automated Processing:** Processes all images in a batch effortlessly.
- **Visual Deliverables:** Outputs clean, side-by-side comparative charts ready for presentations.
