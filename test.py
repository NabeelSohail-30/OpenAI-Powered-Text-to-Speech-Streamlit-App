import openai
import os
from dotenv import load_dotenv, find_dotenv

# Load the environment variables from the .env file
load_dotenv(find_dotenv())
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Define a prompt for the OpenAI Chat API
prompt = """
Please tell me some key importants about data science
"""

# Use OpenAI's ChatCompletion API to generate a response
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ],
)
# Extract the generated text from the response
generated_text = response['choices'][0]['message']['content']

# Print the generated text
print(generated_text)
