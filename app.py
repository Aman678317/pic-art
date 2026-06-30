import streamlit as st
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from skimage.color import rgb2lab
import io

# The 11 base color categories mapped to typical RGB representations.
COLOR_MAP = {
    'White': (255, 255, 255),
    'Black': (0, 0, 0),
    'Red': (255, 0, 0),
    'Green': (0, 128, 0),
    'Yellow': (255, 255, 0),
    'Blue': (0, 0, 255),
    'Brown': (165, 42, 42),
    'Purple': (128, 0, 128),
    'Pink': (255, 192, 203),
    'Orange': (255, 165, 0),
    'Gray': (128, 128, 128)
}

@st.cache_data
def get_color_lab_array():
    color_names = list(COLOR_MAP.keys())
    color_rgbs = np.array(list(COLOR_MAP.values()), dtype=np.uint8)
    color_rgbs_reshaped = color_rgbs.reshape((1, len(color_names), 3))
    colors_lab = rgb2lab(color_rgbs_reshaped)[0]
    return color_names, colors_lab, color_rgbs

COLOR_NAMES, COLORS_LAB, COLOR_RGBS = get_color_lab_array()

def analyze_image_colors(image):
    # Convert to RGB
    img = image.convert('RGB')
    
    # Resize to speed up calculation
    img.thumbnail((400, 400))
    img_np = np.array(img)
    
    # Convert to LAB
    img_lab = rgb2lab(img_np)
    
    # Flatten
    pixels_lab = img_lab.reshape(-1, 3)
    
    # Calculate distances
    distances = np.linalg.norm(pixels_lab[:, np.newaxis, :] - COLORS_LAB[np.newaxis, :, :], axis=2)
    
    # Find closest color
    closest_color_indices = np.argmin(distances, axis=1)
    
    # Count occurrences
    unique, counts = np.unique(closest_color_indices, return_counts=True)
    
    # Calculate percentages
    total_pixels = len(pixels_lab)
    percentages = {COLOR_NAMES[i]: (count / total_pixels) * 100 for i, count in zip(unique, counts)}
    
    # Sort descending
    sorted_percentages = dict(sorted(percentages.items(), key=lambda item: item[1], reverse=True))
    
    return sorted_percentages

st.set_page_config(page_title="Pic-Art Color Analysis", layout="wide")

st.title("🎨 Pic-Art Image Color Analysis")
st.markdown("Upload an image to analyze its pixel-level color distribution across 11 primary categories using perceptual color distance (CIELAB).")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original Image")
        # Support for new streamlit version api
        st.image(image, use_container_width=True)
        
    with col2:
        st.subheader("Color Percentage Breakdown")
        with st.spinner("Analyzing colors..."):
            percentages = analyze_image_colors(image)
            
            # Prepare pie chart
            labels = list(percentages.keys())
            sizes = list(percentages.values())
            
            plot_colors = []
            for label in labels:
                rgb = COLOR_MAP[label]
                plot_colors.append(f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}")
            
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(sizes, labels=[f"{l} ({s:.1f}%)" for l, s in zip(labels, sizes)], 
                    colors=plot_colors, startangle=140, 
                    wedgeprops={'edgecolor': 'black', 'linewidth': 1})
            ax.axis('equal')
            
            # Transparent background for the figure
            fig.patch.set_alpha(0.0)
            
            st.pyplot(fig)
            
    st.subheader("Detailed Breakdown")
    # Show as progress bars
    for color, pct in percentages.items():
        rgb = COLOR_MAP[color]
        hex_color = f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
        st.markdown(f"**{color}** ({pct:.2f}%)")
        st.markdown(
            f"""
            <div style="width: 100%; background-color: #f0f2f6; border-radius: 5px;">
                <div style="width: {pct}%; height: 20px; background-color: {hex_color}; border-radius: 5px; border: 1px solid #ccc;"></div>
            </div>
            """, 
            unsafe_allow_html=True
        )
