import os
import argparse
from call_function import call_function
from dotenv import load_dotenv
from google import genai
from google.genai import types
from generate_response import generate_response


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("no api_key found")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
client = genai.Client(api_key=api_key)
response = generate_response(client, messages)

if response.usage_metadata is None:
    raise RuntimeError("FAILED API REQUEST")
prompt_token_count = response.usage_metadata.prompt_token_count
candidates_token_count = response.usage_metadata.candidates_token_count
if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {prompt_token_count}")
    print(f"Response tokens: {candidates_token_count}")
    print("Response:")

if response.function_calls:
    function_result_list = []
    for function_call in response.function_calls:
        function_call_result = call_function(function_call, verbose=args.verbose)
        if not function_call_result.parts:
            raise Exception("Error: Function call contains no parts!")
        if not function_call_result.parts[0].function_response:
            raise Exception(
                "Error: function_call_result is missing part[0].function_response"
            )
        if not function_call_result.parts[0].function_response.response:
            raise Exception(
                "Error: function_call_result is missing part[0].function_response.response"
            )
        function_result_list.append(function_call_result.parts[0])
        if args.verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
else:
    print(response.text)


def main():
    pass


if __name__ == "__main__":
    main()
