import gradio as gr
from agent import CustomerAgent
from voice_processing import VoiceProcessor
from pathlib import Path

# Initialize components
agent = CustomerAgent()
voice_processor = VoiceProcessor()

def process_input(audio_path: str, text_query: str) -> str:
    """Handle both voice and text input"""
    try:
        if audio_path:
            # Just use the original file without copying
            query = voice_processor.transcribe(audio_path)
            print(f"Transcribed: {query}")
        else:
            query = text_query

        return agent.query(query) if query else "Please provide input"
    except Exception as e:
        return f"Error: {str(e)}"

def create_interface():
    with gr.Blocks() as app:
        gr.Markdown("## Customer Service AI")

        with gr.Tab("Voice"):
            voice = gr.Audio(sources=["microphone"], type="filepath")
            voice_btn = gr.Button("Process")

        with gr.Tab("Agent Response"):
            text = gr.Textbox()
            text_btn = gr.Button("Process")

        output = gr.Textbox()

        voice_btn.click(process_input, [voice, gr.Textbox(visible=False)], outputs=output)
        text_btn.click(process_input, [gr.Audio(visible=False), text], outputs=output)

    return app

if __name__ == "__main__":
    interface = create_interface()
    interface.launch()