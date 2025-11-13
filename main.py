import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import available_functions, call_function


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=sys.argv[1])])]
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    for _ in range(20):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )
        except Exception as e:
            print(f"Error: {e}")
            break

        for candidate in response.candidates:
            if candidate.content is not None:
                messages.append(candidate.content)

        match sys.argv[2:]:
            case ["--verbose"]:
                if response.function_calls:
                    for function_call_part in response.function_calls:
                        function_call_result = call_function(
                            function_call_part, verbose=True
                        )
                        print(
                            f"-> {function_call_result.parts[0].function_response.response}"
                        )

                        messages.append(
                            types.Content(parts=function_call_result.parts, role="user")
                        )
                else:
                    print(f"User prompt: {response.text}")
                    print(
                        f"Prompt tokens: {response.usage_metadata.prompt_token_count}"
                    )
                    print(
                        f"Response tokens: {response.usage_metadata.candidates_token_count}"
                    )
                    break
            case _:
                if response.function_calls:
                    for function_call_part in response.function_calls:
                        function_call_result = call_function(function_call_part)

                        messages.append(
                            types.Content(parts=function_call_result.parts, role="user")
                        )
                else:
                    print("Final response:")
                    print(response.text)
                    break


if __name__ == "__main__":
    main()
