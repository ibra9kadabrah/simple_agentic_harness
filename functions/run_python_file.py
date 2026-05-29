import os 
import subprocess
from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="run a python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file_path, relative to the working directory(default is working directory itself"
            ),
            "args":types.Schema(
                type=types.Type.ARRAY,
                description="args, an array of items that are types.Type.STRING",
                items=types.Schema(
                    type=types.Type.STRING
                ),
            ),
        }
    )
)


def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    abs_path = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(abs_path, file_path))
    valid_target_path = os.path.commonpath([abs_path, target_path]) == abs_path

    if not valid_target_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    
    if not target_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    
    command = ["python", target_path]
    if not args == None:
        command.extend(args)
    try:
        completed = subprocess.run(command, capture_output=True, 
                                cwd=os.path.dirname(target_path), text=True, timeout=30)
        
        result_str = ""
        if completed.returncode:
            result_str += "Process exited with code X"
        if not completed.stdout and not completed.stderr:
            result_str += "No output produced"
        if completed.stderr:
            result_str += f"STDERR: {completed.stderr}"
        if completed.stdout:
            result_str += f"STDOUT: {completed.stdout}"
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
    return result_str