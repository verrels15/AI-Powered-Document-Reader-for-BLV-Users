import gradio as gr
import os
from datetime import datetime
from gtts import gTTS
from core.ocr import extract_text_from_image, extract_text_from_pdf

def process_image(file, voice_type="FEMALE US"):
    """Process uploaded image and generate speech with selected voice"""
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)
    
    filename = os.path.basename(file.name)
    save_path = os.path.join("uploads", filename)
    os.rename(file.name, save_path)
    
    try:
        # Extract text
        if filename.lower().endswith('.pdf'):
            final_text = extract_text_from_pdf(save_path)
        else:
            final_text = extract_text_from_image(save_path)
        
        if not final_text.strip():
            return "NO TEXT COULD BE EXTRACTED.", None, gr.update(visible=False), gr.update(visible=False)
        
        # Configure voice parameters
        lang = 'en'
        tld = 'com'  # Default (US English)
        
        # Map UI selection to gTTS parameters
        if voice_type == "FEMALE US":
            tld = 'com'  # US English (female)
        elif voice_type == "FEMALE AU":
            tld = 'com.au'  # Australian English (female)
        elif voice_type == "UK ENGLISH":
            tld = 'co.uk'  # British English
        
        # Generate speech (removed speed parameter)
        tts = gTTS(
            text=final_text,
            lang=lang,
            tld=tld,
            slow=False  # Fixed at normal speed
        )
        
        mp3_filename = f"{os.path.splitext(filename)[0]}_{voice_type.lower().replace(' ', '_')}.mp3"
        mp3_path = os.path.join("outputs", mp3_filename)
        tts.save(mp3_path)
        
        # Status message (removed speed reference)
        message = f"""
        IMAGE '{filename.upper()}' PROCESSED SUCCESSFULLY!
        VOICE: {voice_type.upper()}
        
        EXTRACTED TEXT:
        {final_text[:500].upper()}{'... [TRUNCATED]' if len(final_text) > 500 else ''}
        """
        return message, mp3_path, gr.update(value=mp3_path, visible=True), gr.update(value=mp3_path, visible=True)
    
    except Exception as e:
        return f"ERROR: {str(e).upper()}", None, gr.update(visible=False), gr.update(visible=False)

# Gradio UI with updated voice options
with gr.Blocks(
    theme=gr.themes.Soft(),
    css="""
    .gradio-container * {
        text-transform: uppercase !important;
        font-weight: bold !important;
    }
    """
) as demo:
    gr.Markdown("# IMAGE TO SPEECH CONVERTER")
    gr.Markdown("UPLOAD AN IMAGE TO EXTRACT TEXT AND CONVERT IT TO SPEECH")
    
    with gr.Row():
        file_input = gr.File(label="UPLOAD IMAGE", file_types=[".jpg", ".jpeg", ".png", ".pdf"])
    
    with gr.Row():
        voice_type = gr.Dropdown(
            label="VOICE TYPE",
            choices=["FEMALE US", "FEMALE AU", "UK ENGLISH"],  # Updated options
            value="FEMALE US"  # New default
        )
    
    audio_output = gr.Audio(label="GENERATED SPEECH", visible=False, interactive=False)
    output_text = gr.Textbox(label="PROCESSING STATUS")
    download_button = gr.DownloadButton(label="DOWNLOAD MP3", visible=False)

    file_input.upload(
        fn=process_image,
        inputs=[file_input, voice_type],  # Removed speed input
        outputs=[output_text, audio_output, audio_output, download_button]
    )
    
    download_button.click(
        fn=lambda x: x,
        inputs=audio_output,
        outputs=download_button
    )

if __name__ == "__main__":
    demo.launch()