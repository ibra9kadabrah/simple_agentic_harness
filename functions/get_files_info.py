import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory," \
    "providing file sizes and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory(default is working directory itself)"
            )
        }
    )
)

def get_files_info(working_directory, directory="."):
    abs_path = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(abs_path, directory))
    valid_target_path = os.path.commonpath([abs_path, target_path]) == abs_path
    
    if not valid_target_path:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_path):
        return f'Error: "{directory}" is not a directory'
    
    # iterate over items in target dir, for each , record name, file_size, is it a dir?
    result_string = ""
    try:
        dir = os.listdir(target_path)
        for item in dir:
            item_path = os.path.join(target_path, item)
            is_dir = os.path.isdir(item_path)
            size = os.path.getsize(item_path)
            result_string += f"- {item}: file_size={size}, is_dir={is_dir}\n"
    except Exception as e:
        raise Exception(f"Error: {e}")   
    
    return result_string

