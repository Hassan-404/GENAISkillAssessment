from config import Config
import whisper
import os


class VoiceProcessor:
    def __init__(self, model_size="small"):
        """Initialize with optional custom FFmpeg path"""
        whisper.ffmpeg_path = "ffmpeg.exe"
        self.model = whisper.load_model(model_size)

    def transcribe(self, audio_path):
        try:
            if not os.path.exists(audio_path):
                raise FileNotFoundError(f"Audio file not found: {audio_path}")
            result = self.model.transcribe(audio_path)
            return {
                "text": result["text"],
                "language": result.get("language", "unknown")
            }
        except Exception as e:
            return {"error": str(e)}


# if __name__ == "__main__":
#     processor = VoiceProcessor(
#         model_size="base",
#     )
#
#     result = processor.transcribe(
#         r"C:\Users\Hassan X\PycharmProjects\Assessment\data\recordings\sample.wav"
#     )
#
#     if "error" in result:
#         print(f"Error: {result['error']}")
#     else:
#         print(f"Transcript: {result['text']}")
#         print(f"Language: {result['language']}")