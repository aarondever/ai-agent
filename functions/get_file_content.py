import os

from google.genai import types

import config

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Return content in specific file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The name of the file, relative to the working directory.",
            ),
        },
    ),
)


def get_file_content(working_directory: str, file_path: str) -> str:
    file_abs_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not file_abs_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(file_abs_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(file_abs_path, "r") as f:
            content = f.read(config.MAX_CHARS)
            if os.path.getsize(file_abs_path) > config.MAX_CHARS:
                return (
                    content
                    + f'[...File "{file_path}" truncated at {config.MAX_CHARS} characters]'
                )
            return content

    except Exception as e:
        return f"Error: {e}"
