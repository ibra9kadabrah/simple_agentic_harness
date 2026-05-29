import os
import sys as sys
import argparse as argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions

def main():
    
    load_dotenv()
    key = os.environ.get("GEMINI_API_KEY")

    if not key:
        raise RuntimeError("api key not found")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # each message is of type content. we have a list off message, each message has a role, and the actual texts, a list of type Part than be text or other
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    client = genai.Client(api_key = key)
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
        )
    except Exception as e:
        raise RuntimeError(f"api call failed: {e}")

    
    if args.verbose:
        if response.usage_metadata:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        else:
            raise RuntimeError("response usage_metadata is None")

    try:
        if response.function_calls != None:
            for call in response.function_calls:
                print(f"Calling function: {call.name}({call.args})")
        else:
            print(f"Response: \n{response.text}")
            
    except ValueError as e:
        raise RuntimeError(f"Problem with response text: {e}")

if __name__ == "__main__":
    main()

