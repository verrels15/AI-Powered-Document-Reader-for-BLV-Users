import os
import sys

# Add the current directory to the system path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from core.ocr import extract_text_from_image, extract_text_from_pdf

# print("Extracted text from sample.jpg:")
# print(extract_text_from_image("sample.jpg"))

print("Extracted text from sample.pdf:")
print(extract_text_from_pdf("sample.pdf"))

