from PIL import Image
import pytesseract

# Load a sample image (replace with your own image file)
image = Image.open("images.jpeg")  # Put an image file in the same folder

# Run OCR
text = pytesseract.image_to_string(image)

# Print the extracted text
print("Extracted Text:\n", text)
