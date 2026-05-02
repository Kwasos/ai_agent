import os
import argparse
from dotenv import load_dotenv
from google import genai


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("no api_key found")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.5-flash", contents=args.user_prompt
)
if response.usage_metadata is None:
    raise RuntimeError("failed API request")
prompt_token_count = response.usage_metadata.prompt_token_count
candidates_token_count = response.usage_metadata.candidates_token_count
print(f"User prompt: {args.user_prompt}")
print(f"Prompt tokens: {prompt_token_count}")
print(f"Response tokens: {candidates_token_count}")
print("Response:")
print(response.text)


def main():
    pass


if __name__ == "__main__":
    main()
