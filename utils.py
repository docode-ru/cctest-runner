import sys
import json

import subprocess
from typing import Callable, Optional


def get_interpreter_path(interpreter: str) -> str:
    result = subprocess.run(['which', interpreter], capture_output=True, text=True)
    return result.stdout.strip()


def compile_java(java_file):
    javac_command = ["javac", java_file]
    proc = subprocess.Popen(javac_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()

    if proc.returncode != 0:
        print(f"Error compiling {java_file}: {err.decode()}")
        raise Exception("Compilation Error")

def to_bytearray(s):
    return bytearray(bytes(s, 'utf-8')).replace(b'\\n', b'\n')

def run_code(path, input=None, interpreter='python'):

    proc = subprocess.Popen(
        ' '.join([interpreter, str(path)]),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        shell=True
    )

    input_data = to_bytearray('\n'.join(map(str, input))) if input else None

    try:
        stdout, stderr = proc.communicate(input=input_data, timeout=1)

        return "\n".join(stdout.decode("utf-8").strip().splitlines()), stderr.decode("utf-8")
    except subprocess.TimeoutExpired:
        proc.kill()
        return (bytes('', 'utf-8'), bytes('Execution Timeout', 'utf-8'))
    except Exception as e:
        return (bytes('', 'utf-8'), bytes(str(e), 'utf-8'))


def run_test(path, exp_output=None, input=None):
    
    # load interpreter from settings
    interpreter = load_settings().get('interpreter', 'python')

    output, error = run_code(path, input=input, interpreter=interpreter)

    if error:
        return None, error
    assert output == exp_output, "Expected '{}' but got '{}' for input: '{}'".format(exp_output, output, input)
    return output, None

def run_test_data(path, test_data):
    """
    Run test data and return error if any
    """
    for user_input, expected_output in test_data:
        output, error = run_test(path, exp_output=expected_output, input=user_input)
        if error:
            return None, error
    return f"Tests passed successfully", None

def has_function(path, function_name):
    """
    Check if file contains function definition with function name on given path
    """
    with open(path) as f:
        if path.endswith('.py'):
            return f'def {function_name}' in f.read()
        elif path.endswith('.js'):
            return f'function {function_name}' in f.read()
        return function_name in f.read()

# decorator that checks if a function is defined in a file and gets func name from function name
def check_contains_function(function_name: Optional[str] = None) -> Callable:
    def decorator(func):
        """Decorator to check if a specific function exists."""
        func_name = function_name or func.__name__.replace("test_", "")
        def wrapper(*args, **kwargs):
            """Wrapper function that checks for the existence of a given function."""
            if not has_function(args[0], func_name):
                return None, f"Function '{func_name}' is not defined"
            return func(*args, **kwargs)
        return wrapper
    return decorator

def save_settings(settings):
    """
    Save the given settings to a JSON file.

    :param settings: The settings to be saved.
    :type settings: dict
    """
    with open('settings.json', 'w') as f:
        json.dump(settings, f)

def load_settings():
    """
    Load the settings from the JSON file.

    :return: The loaded settings.
    :rtype: dict
    """
    with open('settings.json', 'r') as f:
        return json.load(f)
    