#!/usr/bin/env python3
import math
from PIL import Image, ImageDraw

def create_gradient_image(width=300, height=200, output_path="test_image.png"):
    img = Image.new("RGB", (width, height), "black")
    draw = ImageDraw.Draw(img)

    center_x = width // 2
    center_y = height // 2
    max_radius = min(width, height) // 2 - 10
    
    for r in range(max_radius, 0, -1):
        brightness = int(255 * (1 - r / max_radius))
        
        for angle in range(360):
            rad = math.radians(angle)
            x = center_x + int(r * math.cos(rad))
            y = center_y + int(r * math.sin(rad))
            
            h = angle / 360.0
            s = 1.0
            v = 1.0 - (r / max_radius)
            
            i = int(h * 6)
            f = h * 6 - i
            p = v * (1 - s)
            q = v * (1 - f * s)
            t = v * (1 - (1 - f) * s)
            
            if i % 6 == 0:
                red, grn, blu = v, t, p
            elif i % 6 == 1:
                red, grn, blu = q, v, p
            elif i % 6 == 2:
                red, grn, blu = p, v, t
            elif i % 6 == 3:
                red, grn, blu = p, q, v
            elif i % 6 == 4:
                red, grn, blu = t, p, v
            else:
                red, grn, blu = v, p, q
                
            color = (int(red * 255), int(grn * 255), int(blu * 255))
            draw.point((x, y), fill=color)
            
    # Save the image
    img.save(output_path)
    print(f"Test image saved to {output_path}")

if __name__ == "__main__":
    create_gradient_image()
