# Receipt Printer Test

A Python script for testing a Rongta RP326 receipt printer using python-escpos.

## Features

- Basic text formatting (bold, double height, double width, underline)
- Text alignment (left, center, right)
- Barcode printing (CODE39, EAN13)
- QR code generation
- Image printing

## Requirements

- Python 3
- python-escpos
- PIL (Pillow)

## Installation

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install python-escpos pillow
```

## Usage

Edit the IP address in `test_printer.py` if your printer is at a different network location.

```bash
python test_printer.py
```