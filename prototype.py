import os
import glob
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from skimage.color import rgb2lab

# The 11 base color categories mapped to specific Hex to RGB representations.
COLOR_MAP = {
    'White': (255, 255, 255),    # #FFFFFF
    'Black': (0, 0, 0),          # #000000
    'Red': (255, 0, 0),          # #FF0000
    'Green': (0, 166, 81),       # #00A651
    'Yellow': (255, 215, 0),     # #FFD700
    'Blue': (0, 102, 255),       # #0066FF
    'Brown': (139, 69, 19),      # #8B4513
    'Purple': (128, 0, 128),     # #800080
    'Pink': (255, 105, 180),     # #FF69B4
    'Orange': (255, 140, 0),     # #FF8C00
    'Gray': (128, 128, 128)      # #808080
}

def get_color_lab_array():
    color_names = list(COLOR_MAP.keys())
    color_rgbs = np.array(list(COLOR_MAP.values()), dtype=np.uint8)
    color_rgbs_reshaped = color_rgbs.reshape((1, len(color_names), 3))
    colors_lab = rgb2lab(color_rgbs_reshaped)[0]
    return color_names, colors_lab, color_rgbs

COLOR_NAMES, COLORS_LAB, COLOR_RGBS = get_color_lab_array()

def analyze_image_colors(image):
    """
    Analyzes the image and returns a dictionary of colors and their percentages.
    """
    # Convert to RGB just in case it's RGBA or Grayscale
    img = image.convert('RGB')
    
    # Resize to speed up calculation without significantly altering proportions
    img.thumbnail((400, 400))
    img_np = np.array(img)
    
    # Convert image to LAB color space for better perceptual distance measurement
    img_lab = rgb2lab(img_np)
    
    # Flatten the image to a 1D list of pixels
    pixels_lab = img_lab.reshape(-1, 3)
    
    # Calculate Euclidean distance (Delta E CIE76) between all pixels and the 11 target colors
    distances = np.linalg.norm(pixels_lab[:, np.newaxis, :] - COLORS_LAB[np.newaxis, :, :], axis=2)
    
    # Find the index of the closest target color for each pixel
    closest_color_indices = np.argmin(distances, axis=1)
    
    # Count occurrences of each color
    unique, counts = np.unique(closest_color_indices, return_counts=True)
    
    # Calculate percentages
    total_pixels = len(pixels_lab)
    percentages = {COLOR_NAMES[i]: (count / total_pixels) * 100 for i, count in zip(unique, counts)}
    
    # Sort descending
    sorted_percentages = dict(sorted(percentages.items(), key=lambda item: item[1], reverse=True))
    
    return sorted_percentages

def main():
    import sys
    print("Starting Image Color Analysis Prototype...")
    
    # If arguments are passed, use them as image files
    if len(sys.argv) > 1:
        image_files = sys.argv[1:]
    else:
        # Find all images in the current directory
        extensions = ['*.jpg', '*.jpeg', '*.png']
        image_files = []
        for ext in extensions:
            image_files.extend(glob.glob(ext))
            image_files.extend(glob.glob(ext.upper()))
            
    if not image_files:
        print("No image files (.jpg, .png) found in the current directory.")
        print("Please place the images in this folder and run again.")
        return
        
    for img_path in image_files:
        if img_path.startswith("chart_"):
            continue # Skip generated charts
            
        print(f"\nProcessing {img_path}...")
        
        try:
            img = Image.open(img_path)
            percentages = analyze_image_colors(img)
            
            # Create a side-by-side plot
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
            
            # Show original image
            ax1.imshow(img)
            ax1.axis('off')
            ax1.set_title("Original Image")
            
            # Prepare pie chart
            labels = list(percentages.keys())
            sizes = list(percentages.values())
            
            # Map colors for matplotlib
            plot_colors = []
            for label in labels:
                rgb = COLOR_MAP[label]
                plot_colors.append(f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}")
            
            # Plot pie chart
            ax2.pie(sizes, labels=[f"{l} ({s:.1f}%)" for l, s in zip(labels, sizes)], 
                    colors=plot_colors, startangle=140, 
                    wedgeprops={'edgecolor': 'black', 'linewidth': 1})
            ax2.axis('equal')
            ax2.set_title("Color Percentage Breakdown")
            
            # Save the chart
            output_filename = f"chart_{os.path.splitext(os.path.basename(img_path))[0]}.pdf"
            plt.savefig(output_filename, bbox_inches='tight', format='pdf')
            print(f"Success! Saved chart to {output_filename}")
            
            # Close plot to free memory
            plt.close(fig)
            
        except Exception as e:
            print(f"Error processing {img_path}: {e}")

if __name__ == "__main__":
    main()
