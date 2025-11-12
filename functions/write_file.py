import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    file_abs_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not file_abs_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        dir = os.path.dirname(file_abs_path)

        if not os.path.exists(dir):
            os.makedirs(dir)

        with open(file_abs_path, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error: {e}"
