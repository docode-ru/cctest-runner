import io
import sys

import subprocess
from typing import Callable, Optional

def to_bytearray(s):
    return bytearray(bytes(s, 'utf-8')).replace(b'\\n', b'\n')

def run_code(path, input=None):
    proc = subprocess.Popen(
        [sys.executable, path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
    )

    stdout, stderr = proc.communicate(input=to_bytearray('\n'.join(input)) if input else None)
    return "\n".join(stdout.decode("utf-8").strip().splitlines()), stderr.decode("utf-8")


def run_test(path, exp_output=None, input=None):
    
    output, error = run_code(path, input=input)

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

