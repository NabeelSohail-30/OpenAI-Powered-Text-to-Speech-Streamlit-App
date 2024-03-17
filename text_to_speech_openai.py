from dotenv import load_dotenv, find_dotenv
from typing import *
from tempfile import NamedTemporaryFile
import os
import openai
from pathlib import Path

# Load the environment variables from the .env file
load_dotenv(find_dotenv())
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def main():
    print('Starting')

    # initialize openai client
    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    print('Client created')

    text = "ہم تیری ہی عبادت کرتے ہیں اور تجھ ہی سے مدد چاہتے ہیں۔ اس سے پہلی آیات میں بیان ہوا کہ ہر طرح کی حمد و ثنا کا حقیقی مستحق اللہ تعالٰی ہے جو کہ سب جہانوں کا پالنے والا، بہت مہربا ن اور رحم فرمانے والا ہے اور اس آیت سے بندوں کو سکھایا جارہا ہے کہ اللہ  تعالٰی کی بارگاہ میں اپنی بندگی کا اظہار یوں کرو کہ اے اللہ !عَزَّوَجَلَّ، ہم صرف تیری ہی عبادت کرتے ہیں کیونکہ عبادت کا مستحق صرف تو ہی ہے اور تیرے علاوہ اور کوئی اس لائق ہی نہیں کہ اس کی عبادت کی جاسکے اور حقیقی مدد کرنے والا بھی تو ہی ہے۔تیری اجازت و مرضی کے بغیر کوئی کسی کی کسی قسم کی ظاہری، باطنی، جسمانی روحانی، چھوٹی بڑی کوئی مدد نہیں کرسکتا"

    speech_file_path = Path(__file__).parent / "speech_urdu_openai_v2.mp3"

    response = client.audio.speech.create(
        model="tts-1-hd",
        voice="alloy",
        input=text
    )

    print('Response created')

    response.stream_to_file(speech_file_path)


if __name__ == "__main__":
    main()
