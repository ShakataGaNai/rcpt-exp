#!/usr/bin/env python
from escpos.printer import Network
import qrcode
from PIL import Image
import time
import os

def main():
    """Test script for Rongta RP326 receipt printer."""
    try:
        # Connect to the printer
        print("Connecting to printer at 10.23.22.96...")
        printer = Network("10.23.22.96")
        
        # Print header
        printer.set(align='center')
        printer.text("RECEIPT PRINTER TEST\n")
        printer.text("Rongta RP326\n")
        printer.text("=" * 32 + "\n\n")
        
        # Basic text styles
        printer.set(align='left')
        printer.text("BASIC TEXT STYLES\n")
        printer.text("-" * 32 + "\n")
        
        # Normal text
        printer.text("Normal text\n")
        
        # Bold text
        printer.set(bold=True)
        printer.text("Bold text\n")
        printer.set(bold=False)
        
        # Double height
        printer.set(double_height=True)
        printer.text("Double height\n")
        printer.set(double_height=False)
        
        # Double width
        printer.set(double_width=True)
        printer.text("Double width\n")
        printer.set(double_width=False)
        
        # Underline
        printer.set(underline=1)
        printer.text("Underlined text\n")
        printer.set(underline=0)
        
        # Inverted colors (if supported)
        try:
            printer.set(text_type="B")
            printer.text("Inverted colors\n")
            printer.set(text_type="normal")
        except:
            printer.text("Inverted colors not supported\n")
        
        printer.text("\n")
        
        # Alignment demo
        printer.text("ALIGNMENT DEMO\n")
        printer.text("-" * 32 + "\n")
        
        printer.set(align='left')
        printer.text("Left aligned\n")
        
        printer.set(align='center')
        printer.text("Center aligned\n")
        
        printer.set(align='right')
        printer.text("Right aligned\n")
        
        printer.set(align='left')
        printer.text("\n")
        
        # Barcode demo
        printer.text("BARCODE DEMO\n")
        printer.text("-" * 32 + "\n")
        
        # Code39 barcode
        printer.set(align='center')
        printer.barcode("123456789", "CODE39", height=100, width=2)
        printer.text("\nCODE39: 123456789\n\n")
        
        # EAN13 barcode
        printer.barcode("5901234123457", "EAN13", height=100, width=2)
        printer.text("\nEAN13: 5901234123457\n\n")
        
        printer.set(align='left')
        
        # QR code demo
        printer.text("QR CODE DEMO\n")
        printer.text("-" * 32 + "\n")
        
        printer.set(align='center')
        printer.qr("https://github.com/python-escpos/python-escpos", size=8)
        printer.text("\nQR: python-escpos GitHub\n\n")
        
        # Image demo
        printer.text("IMAGE DEMO\n")
        printer.text("-" * 32 + "\n")
        
        # Create a simple test image
        img = Image.new('RGB', (400, 200), color=(255, 255, 255))
        
        # Draw some text
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("Arial", 30)
        except IOError:
            # Fallback to default font
            font = ImageFont.load_default()
        
        draw.text((10, 10), "Image Test", fill=(0, 0, 0), font=font)
        draw.rectangle([(20, 50), (380, 150)], outline=(0, 0, 0), width=5)
        draw.ellipse([(50, 70), (350, 130)], outline=(0, 0, 0), width=5)
        
        # Save the image temporarily
        img_path = "test_image.png"
        img.save(img_path)
        
        # Print the image
        printer.set(align='center')
        printer.image(img_path)
        printer.text("\nTest Image\n\n")
        
        # Clean up
        try:
            os.remove(img_path)
        except:
            pass
        
        # Footer
        printer.set(align='center')
        printer.text("=" * 32 + "\n")
        printer.text("Test completed at\n")
        printer.text(time.strftime("%Y-%m-%d %H:%M:%S") + "\n")
        printer.text("Thank you!\n\n\n\n")
        
        # Cut paper
        printer.cut()
        
        print("Test completed successfully.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()