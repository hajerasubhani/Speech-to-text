import io
import time

import speech_recognition as sr
import streamlit as st

st.set_page_config(page_title="Speech to Text", page_icon="🎤")

st.title("🎤 Speech-to-Text Application")
st.write("Record your voice and convert it into text.")

LANGUAGES = {
    "Arabic (UAE)": "ar-AE",
    "Arabic (Saudi Arabia)": "ar-SA",
    "Arabic (Egypt)": "ar-EG",
    "English (US)": "en-US",
}
language_name = st.selectbox("Language", list(LANGUAGES.keys()))
language = LANGUAGES[language_name]


def transcribe(audio_data, language, retries=3):
    recognizer = sr.Recognizer()
    last_error = None
    for attempt in range(retries):
        try:
            return recognizer.recognize_google(audio_data, language=language)
        except (sr.RequestError, OSError) as e:  # OSError covers WinError 10054
            last_error = e
            time.sleep(1.5)
    raise sr.RequestError(f"Connection failed after {retries} attempts: {last_error}")


audio_value = st.audio_input("🎙️ Record your voice")

if audio_value is not None:
    st.audio(audio_value)

    with st.spinner("Processing..."):
        try:
            recognizer = sr.Recognizer()
            with sr.AudioFile(io.BytesIO(audio_value.getvalue())) as source:
                audio_data = recognizer.record(source)

            text = transcribe(audio_data, language)

            st.success("Speech converted successfully!")
            st.text_area("Transcribed Text", text, height=150)

        except sr.UnknownValueError:
            st.error("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            st.error(f"Speech recognition service error: {e}")
        except Exception as e:
            st.error(f"Error: {e}")