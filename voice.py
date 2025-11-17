import tempfile
import speech_recognition as sr
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from gtts import gTTS

router = APIRouter()

# -------------------------------------------------------------
# 1) Voice → Text (Audio to Text)
# -------------------------------------------------------------
@router.post("/voice_to_text")
async def voice_to_text(file: UploadFile = File(...)):
    try:
        # Save uploaded audio file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(await file.read())
            audio_path = temp_audio.name

        recognizer = sr.Recognizer()

        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)

        # Convert audio to text
        text = recognizer.recognize_google(audio_data)

        return {"text": text}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Voice processing failed: {str(e)}")


# -------------------------------------------------------------
# 2) Text → Voice (Text to Audio MP3 Download)
# -------------------------------------------------------------
@router.post("/voice_reply")
async def voice_reply(text: str):
    try:
        # Convert given text to speech
        tts = gTTS(text=text, lang="en")

        output_file = "reply.mp3"
        tts.save(output_file)

        return FileResponse(
            output_file,
            media_type="audio/mpeg",
            filename="reply.mp3"
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Voice reply failed: {str(e)}")
