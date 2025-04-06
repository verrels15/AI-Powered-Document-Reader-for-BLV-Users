import os
import sys

# Add the current directory to the system path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from core.ocr import extract_text_from_image, extract_text_from_pdf

# === Validate input from terminal ===
if len(sys.argv) != 2:
    print("❌ Usage: python program.py <path_to_file>")
    sys.exit(1)

input_file = sys.argv[1]

if not os.path.exists(input_file):
    print(f"❌ File not found: {input_file}")
    sys.exit(1)

# === Create outputs/ folder ===
os.makedirs("outputs", exist_ok=True)

# === Determine file type ===
ext = os.path.splitext(input_file)[1].lower()

if ext == ".pdf":
    print(f"📄 Extracting text from PDF: {input_file}")
    extracted_text = extract_text_from_pdf(input_file)
elif ext in [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".gif"]:
    print(f"🖼️ Extracting text from image: {input_file}")
    extracted_text = extract_text_from_image(input_file)
else:
    print("❌ Unsupported file type. Only PDF and common image formats are supported.")
    sys.exit(1)

# === Auto-increment output filename ===
def get_next_output_filename(folder, base_name="output", ext=".txt"):
    i = 0
    while True:
        filename = f"{base_name}{i}{ext}"
        full_path = os.path.join(folder, filename)
        if not os.path.exists(full_path):
            return full_path
        i += 1

output_path = get_next_output_filename("outputs")

# === Write extracted text to output file ===
with open(output_path, "w", encoding="utf-8") as f:
    f.write(extracted_text)

print(f"✅ Text successfully written to {output_path}")
