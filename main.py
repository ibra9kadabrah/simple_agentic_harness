import os
import sys as sys
import argparse as argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    
    load_dotenv()
    key = os.environ.get("GEMINI_API_KEY")

    if not key:
        raise RuntimeError("api key not found")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    client = genai.Client(api_key = key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    MAX_ITERATIONS = 20

    for i in range(0, MAX_ITERATIONS):

    # each message is of type content. we have a list off message, each message has a role, and the actual texts, a list of type Part than be text or other
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
            if response.function_calls:
                function_results_list = []

                for function_call in response.function_calls:
                    function_call_result = call_function(function_call, args.verbose)

                if (function_call_result.parts and 
                function_call_result.parts[0].function_response and 
                function_call_result.parts[0].function_response.response):
                    
                    function_results_list.append(function_call_result.parts[0])
                    messages.append(types.Content(role="user", parts=function_results_list))

                    if response.candidates:
                        for candidate in response.candidates:
                            messages.append(candidate.content)

                    if args.verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                else:
                    raise Exception("invalid function response")
            else:
                print(f"response text: {response.text}")
                return 
                
        except ValueError as e:
            raise RuntimeError(f"Problem with response text: {e}")
        
    print("MAX ITERATIONS REACHED WITHOUT RESPONSE")
    sys.exit(1)



if __name__ == "__main__":
    main()

