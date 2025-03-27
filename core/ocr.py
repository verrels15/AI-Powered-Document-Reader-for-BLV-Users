from PIL import Image
import pytesseract
from pdf2image import convert_from_path


# pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"


'''
Function to help extract text from the image
'''
def extract_text_from_image(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text.strip()

'''
Helps extract the text from the pdf 
'''

# Add poppler_path if needed
def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path, poppler_path="/opt/homebrew/bin")
    all_text = ""
    for i, img in enumerate(images):
        text = pytesseract.image_to_string(img)
        all_text += f"\n--- Page {i + 1} ---\n{text}"
    return all_text.strip()