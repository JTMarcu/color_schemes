"""
This code is a Python script that takes a hex color code as input and calculates various related colors, such as complementary, analogous, and triadic colors.
It then prints these colors in both RGB and hex formats and plots them using Matplotlib.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import colorsys

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb_color):
    return '#{:02x}{:02x}{:02x}'.format(int(rgb_color[0]), int(rgb_color[1]), int(rgb_color[2]))

def get_complementary_color(rgb_color):
    comp_color = (255 - int(rgb_color[0]), 255 - int(rgb_color[1]), 255 - int(rgb_color[2]))
    return comp_color

def get_analogous_colors(rgb_color):
    h, l, s = colorsys.rgb_to_hls(rgb_color[0]/255, rgb_color[1]/255, rgb_color[2]/255)
    analogous1 = colorsys.hls_to_rgb((h + 1/12) % 1, l, s)
    analogous2 = colorsys.hls_to_rgb((h - 1/12) % 1, l, s)
    return (int(analogous1[0]*255), int(analogous1[1]*255), int(analogous1[2]*255)), \
           (int(analogous2[0]*255), int(analogous2[1]*255), int(analogous2[2]*255))

def get_triadic_colors(rgb_color):
    h, l, s = colorsys.rgb_to_hls(rgb_color[0]/255, rgb_color[1]/255, rgb_color[2]/255)
    triadic1 = colorsys.hls_to_rgb((h + 1/3) % 1, l, s)
    triadic2 = colorsys.hls_to_rgb((h - 1/3) % 1, l, s)
    return (int(triadic1[0]*255), int(triadic1[1]*255), int(triadic1[2]*255)), \
           (int(triadic2[0]*255), int(triadic2[1]*255), int(triadic2[2]*255))

def plot_colors(primary_color, secondary_colors):
    fig, ax = plt.subplots(1, 4, figsize=(12, 3))
    fig.suptitle('Primary and Secondary Colors')
    
    ax[0].imshow([[np.array(primary_color) / 255]])
    ax[0].axis('off')
    ax[0].set_title('Primary Color')
    ax[0].text(0.5, -0.1, f'RGB: {primary_color}\nHex: {rgb_to_hex(primary_color)}', 
               ha='center', va='center', transform=ax[0].transAxes)
    
    for i, secondary_color in enumerate(secondary_colors):
        ax[i+1].imshow([[np.array(secondary_color) / 255]])
        ax[i+1].axis('off')
        ax[i+1].set_title(f'Secondary Color {i+1}')
        ax[i+1].text(0.5, -0.1, f'RGB: {secondary_color}\nHex: {rgb_to_hex(secondary_color)}', 
                     ha='center', va='center', transform=ax[i+1].transAxes)
    
    plt.tight_layout()
    plt.show()

def main():
    # Ask for hex color input
    hex_color = input("Enter a hex color code (e.g., #3498db): ")
    
    # Convert hex to RGB
    primary_color = hex_to_rgb(hex_color)
    
    # Calculate the complementary color
    complementary_color = get_complementary_color(primary_color)
    
    # Calculate the analogous colors
    analogous_colors = get_analogous_colors(primary_color)
    
    # Calculate the triadic colors
    triadic_colors = get_triadic_colors(primary_color)
    
    primary_color_hex = rgb_to_hex(primary_color)
    complementary_color_hex = rgb_to_hex(complementary_color)
    analogous_colors_hex = [rgb_to_hex(color) for color in analogous_colors]
    triadic_colors_hex = [rgb_to_hex(color) for color in triadic_colors]
    
    # Print the colors
    print(f"Primary Color: RGB {primary_color}, Hex {primary_color_hex}")
    print(f"Complementary Color: RGB {complementary_color}, Hex {complementary_color_hex}")
    print(f"Analogous Colors: RGB {analogous_colors[0]}, Hex {analogous_colors_hex[0]} and RGB {analogous_colors[1]}, Hex {analogous_colors_hex[1]}")
    print(f"Triadic Colors: RGB {triadic_colors[0]}, Hex {triadic_colors_hex[0]} and RGB {triadic_colors[1]}, Hex {triadic_colors_hex[1]}")
    
    # Plot the primary and secondary colors
    plot_colors(primary_color, [complementary_color, analogous_colors[0], triadic_colors[0]])

if __name__ == "__main__":
    main()