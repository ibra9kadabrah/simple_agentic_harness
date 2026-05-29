import os
from config import MAX_CHAR
from google.genai import types


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="get file content in order for you to understand. it reads at MAX_CHAR at a time which 10k chars. it returns an exception in case of error",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file_path to read, relative to the working directory(default is working directory itself)"
            )
        }
    )
)

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




