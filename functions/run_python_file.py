import os
import subprocess

from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_path = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )

        if not valid_target_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path[-3:] == ".py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]

        if args:
            command.extend(args)

        result = subprocess.run(
            command,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30,
        )

        stdout = result.stdout
        stderr = result.stderr
        if not result.returncode == 0:
            if not stdout and not stderr:
                return (
                    f"Process exited with code {result.returncode}"
                    + "\nNo output produced"
                )
            return f"Process exited with code {result.returncode}"

        return f"STDOUT: {stdout}\nSTDERR: {stderr}"

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the python code of the specified file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Required. File path of the python file, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional. Arguments to be used with the command.",
            ),
        },
        required=["file_path"],
    ),
)
