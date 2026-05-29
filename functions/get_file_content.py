import os
from config import MAX_CHAR

def get_file_content(working_directory, file_path):
    abs_path = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(abs_path, file_path))
    valid_target_path = os.path.commonpath([abs_path, target_path]) == abs_path

    if not valid_target_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(target_path) as f:
            content = f.read(MAX_CHAR)
            # After reading the first MAX_CHARS...
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHAR} characters]'
            return content
    except Exception as e:
        return f"Error: {e}"




