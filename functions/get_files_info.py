import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    directory_abs_path = os.path.abspath(os.path.join(working_directory, directory))

    if not directory_abs_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(directory_abs_path):
        return f'Error: "{directory}" is not a directory'

    try:
        result = []

        for content in os.listdir(directory_abs_path):
            result.append(
                f"- {content}: file_size={os.path.getsize(os.path.join(directory_abs_path, content))}, is_dir={os.path.isdir(os.path.join(directory_abs_path, content))}"
            )
    except Exception as e:
        return f"Error: {e}"

    return "\n".join(result)
