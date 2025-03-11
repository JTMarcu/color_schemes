"""
Use Case
generate and visualize color variations based on a given base color.

This code could be used in web design or UI/UX design to help designers create color palettes with consistent hover effects. 
By generating lighter and darker variations of a base color, designers can ensure that their color schemes remain visually appealing and accessible. 
The visualization helps in quickly assessing how the colors will look together, and the text color determination ensures readability.
"""

from colormath.color_objects import sRGBColor, HSVColor
from colormath.color_conversions import convert_color
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb_color):
    return '#{:02x}{:02x}{:02x}'.format(*rgb_color)

def generate_hover_colors(base_color, num_options=3):
    if base_color.startswith('#'):
        base_color = hex_to_rgb(base_color)
    else:
        base_color = tuple(int(c) for c in base_color.split(','))

    base_color_obj = sRGBColor(*[c / 255.0 for c in base_color])
    base_color_hex = rgb_to_hex(base_color)

    hover_colors = []
    labels = []
    for i in range(1, num_options + 1):
        lightness_factor = i * 0.05  # Adjust lightness by 5% increments
        saturation_factor = i * 0.05  # Adjust saturation by 5% increments

        # Generate a lighter version
        hsv_color = convert_color(base_color_obj, HSVColor)
        hsv_color.hsv_v = min(hsv_color.hsv_v + lightness_factor, 1.0)
        hsv_color.hsv_s = min(hsv_color.hsv_s + saturation_factor, 1.0)
        lighter_color = convert_color(hsv_color, sRGBColor)
        hover_colors.append(rgb_to_hex((int(lighter_color.rgb_r * 255), int(lighter_color.rgb_g * 255), int(lighter_color.rgb_b * 255))))
        labels.append(f'Lighter by {int(lightness_factor * 100)}%')

        # Generate a darker version
        hsv_color.hsv_v = max(hsv_color.hsv_v - lightness_factor, 0.0)
        hsv_color.hsv_s = max(hsv_color.hsv_s - saturation_factor, 0.0)
        darker_color = convert_color(hsv_color, sRGBColor)
        hover_colors.append(rgb_to_hex((int(darker_color.rgb_r * 255), int(darker_color.rgb_g * 255), int(darker_color.rgb_b * 255))))
        labels.append(f'Darker by {int(lightness_factor * 100)}%')

    return base_color_hex, hover_colors, labels

def determine_text_color(bg_color):
    bg_color = hex_to_rgb(bg_color)
    luminance = (0.299 * bg_color[0] + 0.587 * bg_color[1] + 0.114 * bg_color[2]) / 255
    return 'white' if luminance < 0.5 else 'black'

def plot_colors(base_color, hover_colors, labels, text_color):
    fig, ax = plt.subplots(1, len(hover_colors) + 1, figsize=(15, 5))
    colors = [base_color] + hover_colors
    labels = ['Base Color'] + labels
    
    for i, (color, label) in enumerate(zip(colors, labels)):
        rect = patches.Rectangle((0, 0), 1, 1, facecolor=color)
        ax[i].add_patch(rect)
        ax[i].text(0.5, 0.5, color, color=text_color, fontsize=12, ha='center', va='center')
        ax[i].set_title(label)
        ax[i].axis('off')
    
    plt.show()

def main():
    color_input = input("Enter a hex color code (e.g., #0a0a23) or an RGB color (e.g., 10, 10, 35): ")
    base_color, hover_colors, labels = generate_hover_colors(color_input)

    print(f"Base Color: {base_color}")
    print("Hover Colors: ", hover_colors)
    print("Text Color: ", determine_text_color(base_color))

    plot_colors(base_color, hover_colors, labels, determine_text_color(base_color))

if __name__ == "__main__":
    main()