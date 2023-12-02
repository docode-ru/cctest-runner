# CCTest to test user Coding Challenges

## Brief description of the main goal:

The CCTest app is designed to run tests on Python CCTest stored in specific directories. It provides a user interface where users can select directories and files to run tests on. The tests are written in Python and are executed dynamically. The results of the tests are displayed in the Streamlit app.

## How to setup

1. clone the repository:
```bash 
git clone https://github.com/docode-ru/cctest.git
```
2. create a virtual environment:
```bash
python -m venv venv
```
3. activate the virtual environment:
```bash
source venv/bin/activate
```

4. install the requirements:
```bash
pip install -r requirements.txt
```

5. run the Streamlit App
```bash
streamlit run cctest.py
```