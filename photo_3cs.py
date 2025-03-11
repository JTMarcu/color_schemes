'''
extract and visualize the dominant colors from an image.
Use Cases
- Design and Art: Designers can use this tool to extract color palettes from images for use in their projects.
- Data Analysis: Analysts can use it to study color distributions in images.
- Web Development: Developers can use it to generate color schemes for websites based on images.
- Marketing: Marketers can analyze brand colors in images for consistency.
'''


import tkinter as tk
from tkinter import filedialog
from PIL import Image
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
import cv2

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def extract_colors(image_path, num_colors=5, saturation_threshold=100, brightness_threshold=100):
    image = Image.open(image_path).convert('RGB')  # Ensure image is in RGB format
    image = image.resize((600, 400))
    image_np = np.array(image)
    
    # Convert to HSV color space
    image_hsv = cv2.cvtColor(image_np, cv2.COLOR_RGB2HSV)
    
    # Filter out low saturation and low brightness
    mask = (image_hsv[:, :, 1] > saturation_threshold) & (image_hsv[:, :, 2] > brightness_threshold)
    image_np = image_np[mask]
    
    image_np = image_np.reshape((-1, 3))  # Flatten the image array

    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(image_np)
    colors = kmeans.cluster_centers_.astype(int)

    return colors

def plot_colors(colors_list):
    fig, axes = plt.subplots(len(colors_list), 1, figsize=(8, 2 * len(colors_list)), subplot_kw=dict(xticks=[], yticks=[], frame_on=False))
    if len(colors_list) == 1:
        axes = [axes]
    for ax, colors in zip(axes, colors_list):
        for i, color in enumerate(colors):
            ax.add_patch(plt.Rectangle((i / len(colors), 0), 1 / len(colors), 1, color=np.array(color) / 255))
            rgb_str = ', '.join(map(str, map(int, color)))
            ax.text(i / len(colors) + 0.5 / len(colors), 0.5, f'{rgb_str}\n{rgb_to_hex(tuple(color))}', 
                    ha='center', va='center', fontsize=12, color='white' if np.mean(color) < 128 else 'black')
    plt.show()

def main():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    if file_path:
        colors1 = extract_colors(file_path, num_colors=5, saturation_threshold=100, brightness_threshold=100)
        colors2 = extract_colors(file_path, num_colors=5, saturation_threshold=50, brightness_threshold=50)
        colors3 = extract_colors(file_path, num_colors=5, saturation_threshold=0, brightness_threshold=0)
        plot_colors([colors1, colors2, colors3])

if __name__ == "__main__":
    main()