import os
import sys
from gtts import gTTS
from transformers import pipeline

# === Importing custom modules ===
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from core.ocr import extract_text_from_image, extract_text_from_pdf

# === Input Validation ===
if len(sys.argv) != 2:
    print("Usage: python smart_reader.py <path_to_file>")
    sys.exit(1)

input_file = sys.argv[1]
if not os.path.exists(input_file):
    print(f"File not found: {input_file}")
    sys.exit(1)

os.makedirs("outputs", exist_ok=True)

# === Decide which function to use ===
ext = os.path.splitext(input_file)[1].lower()
text = ""

if ext == ".pdf":
    print(f"Extracting from PDF: {input_file}")
    text = extract_text_from_pdf(input_file)

    # === Load summarizer only if needed ===
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    print("Splitting and summarizing text...")

    def chunk_text(text, max_chunk_size=900):
        sentences = text.split(". ")
        chunks, current_chunk = [], ""
        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= max_chunk_size:
                current_chunk += sentence + ". "
            else:
                chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        if current_chunk:
            chunks.append(current_chunk.strip())
        return chunks

    text_chunks = chunk_text(text)

    summaries = []
    for chunk in text_chunks:
        try:
            summary = summarizer(chunk, max_length=60, min_length=30, do_sample=False)[0]['summary_text']
            summaries.append(summary)
        except Exception as e:
            print(f"Skipping chunk due to error: {e}")

    final_text = " ".join(summaries)

elif ext in [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".gif"]:
    print(f"Extracting from image: {input_file}")
    final_text = extract_text_from_image(input_file)

else:
    print("Unsupported file type.")
    sys.exit(1)

# === Save audio to file ===
output_audio_path = os.path.join("outputs", "speech.mp3")
tts = gTTS(final_text)
tts.save(output_audio_path)

print(f"Done! Speech saved to {output_audio_path}")
