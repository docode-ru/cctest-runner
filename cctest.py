import os
import importlib.util
import streamlit as st
import re
from utils import *

st.title('CCTest Runner')

# Define the directory where the test files are stored
TEST_DIR = 'tests'
USER_CHALLENGES_DIR = 'challenges'

def create_directory(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def create_default_file(dir_name, file_name, content):
    with open(os.path.join(dir_name, file_name), 'w') as f:
        f.write(content)

def get_subdirectories(dir_name):
    return [d for d in os.listdir(dir_name) if os.path.isdir(os.path.join(dir_name, d)) and d != '__pycache__']

def get_files(dir_name, extensions):
    is_extension_match = lambda f: any(f.endswith(ext) for ext in extensions)
    return [f for f in os.listdir(dir_name) if is_extension_match(f)]

def create_dropdown(title, options, default_option=None):
    if default_option:
        return st.selectbox(title, options, index=options.index(default_option))

    return st.selectbox(title, options)

def create_checkbox(label, default=False):
    return st.checkbox(label, default)

def create_button(label):
    return st.button(label)

def display_code(file_path):
    st.code(open(file_path).read())

def load_module(file_path):
    spec = importlib.util.spec_from_file_location('module.name', file_path)
    test_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(test_module)
    return test_module

def get_test_functions(module):
    return [f for f in dir(module) if callable(getattr(module, f)) and f.startswith('test_')]

def cleanup_inputs_in_code(path_to_challenge):
    with open(path_to_challenge, 'r') as f:
        code = f.read()
        # check if input() contains some text
        if re.search(r'input\(".*"\)', code):
            code = re.sub(r'input\(".*"\)', 'input()', code)
            with open(path_to_challenge, 'w') as f:
                f.write(code)


# Create directories if they don't exist
create_directory(TEST_DIR)
create_directory(USER_CHALLENGES_DIR)

# Get subdirectories
challenge_subdirs = get_subdirectories(USER_CHALLENGES_DIR)
test_subdirs = get_subdirectories(TEST_DIR)

# Create default subdirectories if they don't exist
if not challenge_subdirs:
    create_directory(os.path.join(USER_CHALLENGES_DIR, 'default'))
    challenge_subdirs = get_subdirectories(USER_CHALLENGES_DIR)

if not test_subdirs:
    create_directory(os.path.join(TEST_DIR, 'default'))
    test_subdirs = get_subdirectories(TEST_DIR)

challenges_tab, settings_tab = st.tabs(['Challenges', 'Settings'])

with challenges_tab:
    # Create dropdown menus
    selected_challenge_subdirectory = create_dropdown(f'Select a challenges subdirectory within "{USER_CHALLENGES_DIR}"', challenge_subdirs)

    if create_checkbox('Select same sub directory for tests', True):
        selected_subdirectory = selected_challenge_subdirectory
    else:
        selected_subdirectory = create_dropdown(f'Select a subdirectory within "{TEST_DIR}"', test_subdirs)

    # Get files
    challenges_files = get_files(os.path.join(USER_CHALLENGES_DIR, selected_challenge_subdirectory), ['.py', '.js'])
    test_files = get_files(os.path.join(TEST_DIR, selected_subdirectory), ['.py', '.js'])

    # Create default files if they don't exist
    if not challenges_files:
        create_default_file(os.path.join(USER_CHALLENGES_DIR, selected_challenge_subdirectory), 'challenge_default.py', 'a = "hello"\n\nb = "world"\n\nprint(a + b)')
        challenges_files = get_files(os.path.join(USER_CHALLENGES_DIR, selected_challenge_subdirectory), ['.py', '.js'])

    if not test_files:
        create_default_file(os.path.join(TEST_DIR, selected_subdirectory), 'test_default.py', 'from utils import run_test_data\n\ndef test_helloworld(path):\n    return run_test_data(path, [ (None, "Hello world") ])')
        test_files = get_files(os.path.join(TEST_DIR, selected_subdirectory), ['.py', '.js'])


    # Select files
    selected_challenge = create_dropdown('Select a challenge file from the directory', challenges_files)

    with st.expander('Other test options'):
        # Display challenge code
        if create_checkbox('Show challenge file'):
            display_code(os.path.join(USER_CHALLENGES_DIR, selected_challenge_subdirectory, selected_challenge))


        selected_test_file = f'test_{selected_challenge}'
        if selected_test_file in test_files and create_checkbox('Set test file for challenge automatically', True):
            selected_test_file = create_dropdown('Select a test file from the directory', test_files, selected_test_file)
        else:
            selected_test_file = create_dropdown('Select a test file from the directory', test_files)

        #selected_test_file = create_dropdown('Select a test file from the directory', test_files, )

    # Display code
    if create_checkbox('Show test file'):
        display_code(os.path.join(TEST_DIR, selected_subdirectory, selected_test_file))

    # Load module
    test_module = load_module(os.path.join(TEST_DIR, selected_subdirectory, selected_test_file))

    # Get test functions
    test_functions = get_test_functions(test_module)


    # Run tests
    if create_button('RUN TEST'):
        for test_function in test_functions:
            try:
                test_func = getattr(test_module, test_function)
                path_to_challenge = os.path.join(os.getcwd(), USER_CHALLENGES_DIR, selected_challenge_subdirectory, selected_challenge)

                cleanup_inputs_in_code(path_to_challenge)
                result, error = test_func(path_to_challenge)

                if error:
                    st.error(f'Test {selected_challenge}.py error:')
                    st.code(error)
                else:
                    st.success(f'{test_function}(): {result}')
            except Exception as e:
                st.error(f'Test {test_function} failed with error: {str(e)}')


with settings_tab:
    settings = {}
    # select langage for tests
    interpreter = create_dropdown('Select language', ['python', 'node run.js'])
    settings['interpreter'] = interpreter

    # save setting buttons
    # Check if the "Save" button has been created
    if create_button('Save'):
    
      # If the "Save" button has been created, call the function to save the settings
        save_settings(settings)

