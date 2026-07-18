#!/usr/bin/env python3
"""
Image to ASCII Art Converter
Converts an image into ASCII art representation for terminal output.
Supports grayscale and true color (24-bit ANSI) modes, custom character sets,
aspect ratio correction, and terminal auto-sizing.
"""

import argparse
import os
import sys
from PIL import Image, ImageEnhance

CHARSETS = {
    'standard': " .:-=+*#%@",
    'detailed': " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$",
    'blocks': " ░▒▓█",
}

def get_terminal_width(fallback: int = 80) -> int:
    """
    Attempts to get the current terminal width.
    Falls back to `fallback` if detection fails.
    """
    try:
        columns, _ = os.get_terminal_size()
        return columns
    except OSError:
        return fallback

def scale_image(img: Image.Image, target_width: int, aspect_ratio_correction: float = 0.55) -> Image.Image:
    """
    Resizes the image to the target width while preserving the aspect ratio
    and adjusting for the vertical-to-horizontal ratio of terminal characters.
    """
    orig_width, orig_height = img.size

    img_aspect = orig_height / orig_width

    target_height = int(target_width * img_aspect * aspect_ratio_correction)
    target_height = max(1, target_height)  # Ensure height is at least 1

    try:
        resample_filter = Image.Resampling.LANCZOS
    except AttributeError:
        resample_filter = Image.LANCZOS
        
    return img.resize((target_width, target_height), resample_filter)

def rgb_to_luminance(r: int, g: int, b: int) -> int:
    """
    Computes luminance from RGB values using standard ITU-R BT.601 formula.
    Result is in range [0, 255].
    """
    return int(0.299 * r + 0.587 * g + 0.114 * b)

def convert_to_ascii(img: Image.Image, charset: str, invert: bool = False, color: bool = False) -> str:
    """
    Converts a resized RGB Pillow Image to ASCII characters.
    If color is True, wraps characters in ANSI true color escape codes.
    """

    char_map = CHARSETS.get(charset, charset)
    if not char_map:
        char_map = CHARSETS['standard']
        

    if invert:
        char_map = char_map[::-1]
        
    num_chars = len(char_map)
    lines = []
    width, height = img.size
    

    pixels = img.load()
    
    for y in range(height):
        line_chars = []
        for x in range(width):
            pixel = pixels[x, y]
            

            if isinstance(pixel, int):

                r = g = b = pixel
            elif len(pixel) >= 3:
                r, g, b = pixel[:3]

                if len(pixel) == 4 and pixel[3] == 0:
                    line_chars.append(" ")
                    continue
            else:

                r = g = b = 0
                

            lum = rgb_to_luminance(r, g, b)
            char_idx = int((lum / 255.0) * (num_chars - 1))
            char = char_map[char_idx]
            
            if color:

                line_chars.append(f"\033[38;2;{r};{g};{b}m{char}")
            else:
                line_chars.append(char)
                

        if color:
            line_chars.append("\033[0m")
            
        lines.append("".join(line_chars))
        
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(
        description="Convert any image to ASCII art and output it to the terminal."
    )
    parser.add_argument("image_path", help="Path to the input image file.")
    parser.add_argument(
        "-w", "--width", 
        type=int, 
        default=None,
        help="Width of the output ASCII art in characters (default: auto-detect terminal width)."
    )
    parser.add_argument(
        "-i", "--invert", 
        action="store_true",
        help="Invert character brightness mapping (useful for light backgrounds)."
    )
    parser.add_argument(
        "-c", "--color", 
        action="store_true",
        help="Output in true 24-bit ANSI color."
    )
    parser.add_argument(
        "-s", "--charset", 
        default="standard",
        help="Character set to use: 'standard', 'detailed', 'blocks', or a custom string of characters."
    )
    parser.add_argument(
        "--contrast", 
        type=float, 
        default=1.0,
        help="Contrast adjustment factor (e.g. 1.5 increases contrast, 0.5 decreases it; default 1.0)."
    )
    parser.add_argument(
        "--aspect", 
        type=float, 
        default=0.55,
        help="Aspect ratio correction factor for terminal characters (default: 0.55)."
    )
    
    args = parser.parse_args()
    

    if not os.path.exists(args.image_path):
        print(f"Error: File not found at '{args.image_path}'", file=sys.stderr)
        sys.exit(1)
        
    try:
        img = Image.open(args.image_path)
    except Exception as e:
        print(f"Error: Unable to open image. {e}", file=sys.stderr)
        sys.exit(1)
        

    if img.mode != 'RGB' and img.mode != 'RGBA':
        img = img.convert('RGB')
        

    if args.contrast != 1.0:
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(args.contrast)
        

    target_width = args.width
    if target_width is None:
        target_width = get_terminal_width()
        

    resized_img = scale_image(img, target_width, args.aspect)
    ascii_art = convert_to_ascii(resized_img, args.charset, args.invert, args.color)
    
    print(ascii_art)

if __name__ == "__main__":
    main()
