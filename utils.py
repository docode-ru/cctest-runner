import io
import sys

import subprocess

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
    return stdout.decode("utf-8").strip(), stderr.decode("utf-8")
    

def run_test(path, exp_output=None, input=None):
    
    output, error = run_code(path, input=input)

    if error:
        return None, error
    assert output == exp_output, "Expected '{}' but got '{}' for input: '{}'".format(exp_output, output, input)
    return output, None

def run_test_data(path, test_data):
    for user_input, expected_output in test_data:
        output, error = run_test(path, exp_output=expected_output, input=user_input)
        if error:
            return None, error
    return f"Tests passed successfully", None