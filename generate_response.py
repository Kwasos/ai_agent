from google.genai import types
from call_function import available_functions
from prompts import system_prompt


def generate_response(client, messages):
    return client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
