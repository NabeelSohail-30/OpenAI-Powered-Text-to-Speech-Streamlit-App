import streamlit as st
import openai
import tempfile
import os
import pydub
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def initialize_openai_client(my_api_key):
    """Initialize the OpenAI client with the provided API key."""
    return openai.OpenAI(api_key=my_api_key)


def text_to_speech(client, text: str, model, voice):
    """Convert text to speech using the OpenAI API."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
        speech_file_path = tmpfile.name
        response = client.audio.speech.create(
            model=model,
            voice=voice,
            input=text
        )
        response.stream_to_file(speech_file_path)
        return speech_file_path


def convert_audio_format(input_path, output_path, format):
    """Convert audio format using pydub."""
    audio = pydub.AudioSegment.from_mp3(input_path)
    audio.export(output_path, format=format)


# Streamlit UI setup


def main():
    st.title("🔊 Text to Speech Converter 📝")
    st.image("https://www.piecex.com/product_image/20190625044028-00000544-image2.png")
    st.markdown("""
    This app converts text to speech using OpenAI's tts-1 or tts-1-hd model.
    Please enter your OpenAI API key on the sidebar. **Do not share your API key with others.**
    """)

    # Select box for model selection
    model = st.sidebar.selectbox("Select Model", ["tts-1", "tts-1-hd"])

    # Select box for voice selection
    voice = st.sidebar.selectbox(
        "Select Voice", ["alloy", "echo", "fable", "onyx", "nova", "shimmer"])

    # Select box for format selection
    format = st.sidebar.selectbox(
        "Select Format", ["mp3", "opus", "aac", "flac", "wav"])

    # Text input from user
    user_input = st.text_area("Enter text to convert to speech",
                              "Hello, welcome to our text-to-speech converter!")

    if st.button("Convert"):
        if not OPENAI_API_KEY:
            st.error("API key is required to convert text to speech.")
        else:
            with st.spinner("Converting text to speech..."):
                try:
                    client = initialize_openai_client(OPENAI_API_KEY)
                    mp3_speech_path = text_to_speech(
                        client, user_input, model, voice)

                    if format != "mp3":
                        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{format}") as tmpfile:
                            convert_audio_format(
                                mp3_speech_path, tmpfile.name, format)
                            speech_path = tmpfile.name
                        os.remove(mp3_speech_path)
                    else:
                        speech_path = mp3_speech_path

                    # Display a link to download the audio file
                    st.audio(open(speech_path, 'rb'), format=format)
                    st.markdown(
                        f'[Download {format.upper()} file]({speech_path})', unsafe_allow_html=True)

                    # Clean up: delete the temporary file after use
                    os.remove(speech_path)
                except Exception as e:
                    st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
