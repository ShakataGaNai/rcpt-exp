#!/usr/bin/env python
from escpos.printer import Network
from PIL import Image, ImageDraw, ImageFont
import argparse
import sys
import os

def create_landscape_text_image(lines, font_size=30, line_spacing=10):
    """
    Create an image with text rotated 90 degrees (landscape orientation).
    The text is first rendered in portrait and then rotated.
    """
    if not lines:
        lines = [""]
    
    # Try to load a font, fall back to default if necessary
    try:
        font = ImageFont.truetype("Arial", font_size)
    except IOError:
        try:
            font = ImageFont.truetype("DejaVuSans", font_size)
        except IOError:
            font = ImageFont.load_default()
    
    # Calculate dimensions for each line
    line_heights = []
    line_widths = []
    
    for line in lines:
        if not line:  # Handle empty lines
            line_heights.append(font_size)
            line_widths.append(0)
            continue
            
        # Get line dimensions
        left, top, right, bottom = font.getbbox(line)
        line_width = right - left
        line_height = bottom - top
        line_heights.append(line_height + line_spacing)
        line_widths.append(line_width)
    
    # Calculate dimensions for the portrait image
    total_height = sum(line_heights) + 40  # Add padding
    max_width = max(line_widths) + 40 if line_widths else 200  # Add padding
    
    # Create a white portrait image
    img = Image.new('RGB', (max_width, total_height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Draw text onto the image
    y_position = 20  # Start with some padding
    for i, line in enumerate(lines):
        draw.text((20, y_position), line, fill=(0, 0, 0), font=font)
        y_position += line_heights[i]
    
    # Rotate the image 90 degrees counter-clockwise for landscape orientation
    landscape_img = img.transpose(Image.ROTATE_90)
    
    return landscape_img

def print_landscape_text(lines, printer_ip="10.23.22.96", font_size=30, line_spacing=10):
    """Print text in landscape orientation on receipt printer"""
    try:
        # Create the image with rotated text
        img = create_landscape_text_image(lines, font_size, line_spacing)
        
        # Save to a temporary file
        temp_path = "temp_landscape.png"
        img.save(temp_path)
        
        # Connect to the printer
        printer = Network(printer_ip)
        
        # Print the image
        printer.set(align='left')
        printer.image(temp_path)
        
        # Cut the paper
        printer.cut()
        
        # Clean up
        try:
            os.remove(temp_path)
        except:
            pass
        
        return True
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description='Print text in landscape orientation on a receipt printer.')
    parser.add_argument('-i', '--ip', default="10.23.22.96", help='IP address of the receipt printer')
    parser.add_argument('-f', '--font-size', type=int, default=30, help='Font size for the text')
    parser.add_argument('-l', '--line-spacing', type=int, default=10, help='Spacing between lines')
    parser.add_argument('-t', '--text', action='append', help='Line of text to print (can be used multiple times)')
    parser.add_argument('--file', help='File containing text to print')
    
    args = parser.parse_args()
    
    # Get text lines from various sources
    lines = []
    
    if args.text:
        lines = args.text
    elif args.file:
        try:
            with open(args.file, 'r') as f:
                lines = f.read().splitlines()
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            return 1
    else:
        # If no text provided, read from stdin
        print("Enter your text line by line. Enter a blank line to finish:")
        while True:
            line = input()
            if not line:
                break
            lines.append(line)
        
        if not lines:
            print("No text provided. Exiting.")
            return 1
    
    # Print the text
    success = print_landscape_text(lines, args.ip, args.font_size, args.line_spacing)
    
    if success:
        print("Text printed successfully in landscape orientation.")
        return 0
    else:
        print("Failed to print text.", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())