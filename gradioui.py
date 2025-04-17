import gradio as gr
import os
from datetime import datetime
from gtts import gTTS
from core.ocr import extract_text_from_image, extract_text_from_pdf  # Import your existing OCR function
import ffmpeg

def process_image(file):
    """Process uploaded image and generate speech using your existing OCR setup"""
    # Create directories if they don't exist
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)
    
    # Get file info
    filename = os.path.basename(file.name)
    file_size = os.path.getsize(file.name) / (1024 * 1024)  # Size in MB
    upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Save uploaded file
    save_path = os.path.join("uploads", filename)
    os.rename(file.name, save_path)
    
    try:
        # Use your existing OCR function
        # if file is pdf, use pdf extraction
        # else use image extraction
        if filename.lower().endswith('.pdf'):
            final_text = extract_text_from_pdf(save_path)
        else:

            final_text = extract_text_from_image(save_path)
        
        if not final_text.strip():
            return "No text could be extracted from the image.", None, gr.update(visible=False), gr.update(visible=False)
        
        # Generate MP3
        tts = gTTS(final_text, lang='en')
        mp3_filename = os.path.splitext(filename)[0] + ".mp3"
        mp3_path = os.path.join("outputs", mp3_filename)
        tts.save(mp3_path)
        
        # Prepare output message
        message = f"""
        Image '{filename}' processed successfully!
        Size: {file_size:.2f} MB
        Time: {upload_time}
        
        Extracted Text:
        {final_text[:500]}{'... [truncated]' if len(final_text) > 500 else ''}
        """
        # Provide download link
        return message, mp3_path, gr.update(value=mp3_path, visible=True), gr.update(value=mp3_path, visible=True)
    
    except Exception as e:
        return f"Error processing file: {str(e)}", None, gr.update(visible=False), gr.update(visible=False)

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# Image to Speech Converter")
    gr.Markdown("Upload an image to extract text and convert it to speech")
    
    with gr.Row():
        file_input = gr.File(label="Upload Image", file_types=[".jpg", ".jpeg", ".png", ".pdf"])
        audio_output = gr.Audio(label="Generated Speech", visible=False)
    
    output_text = gr.Textbox(label="Processing Status")
    download_button = gr.DownloadButton(label="Download MP3", visible=False)

    
    file_input.upload(
        fn=process_image,
        inputs=file_input,
        outputs=[output_text, audio_output, audio_output, download_button]
    )
    
    download_button.click(
        fn=lambda x: x,
        inputs=audio_output,
        outputs=download_button
    )



if __name__ == "__main__":
    demo.launch()