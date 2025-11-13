import os
import subprocess

from google.genai import types


def run_python_file(working_directory: str, file_path: str, args: list[str] = []):
    file_abs_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not file_abs_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(file_abs_path):
        return f'Error: File "{file_path}" not found.'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        completed_process = subprocess.run(
            ["python", file_path, *args],
            timeout=30,
            cwd=working_directory,
            capture_output=True,
            text=True,
        )
    except Exception as e:
        return f"Error: executing Python file: {e}"

    results = [
        f"STDOUT: {completed_process.stdout}",
        f"STDERR: {completed_process.stderr}",
    ]

    if completed_process.returncode != 0:
        results.append(f"Process exited with code {completed_process.returncode}")
    elif completed_process.stdout == "" and completed_process.stderr == "":
        return "No output produced."

    return "\n".join(results)


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)
