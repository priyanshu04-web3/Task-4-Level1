import cv2
import numpy as np

img = cv2.imread("map_captured.png")
print("Image shape:", img.shape)

# Print all unique colors in the image
pixels = img.reshape(-1, 3)
unique_colors = np.unique(pixels, axis=0)
print("Unique colors (BGR):")
for color in unique_colors:
    print(color)
