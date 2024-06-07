# CCTest to test user Coding Challenges

## Brief description of the main goal:

The CCTest app is designed to test students challenges in specific directories. It provides a user interface where users can select directories and files to run tests on. The tests are written in Python and are executed dynamically. The results of the tests are displayed in the Streamlit app.


## How to run on windows
You can just run `run.bat` file to install portable python and missing dependencies


## How to setup

1. clone the repository:
```bash 
git clone https://github.com/docode-ru/cctest.git
```
2. create a virtual environment if it doesn't exist:
```bash
python -m venv venv
```
3. activate the virtual environment:
```bash
source venv/bin/activate
```

4. install the app requirements:
```bash
pip install -r requirements.txt
```

5. run the Streamlit App
```bash
streamlit run cctest.py
```

## How to JavaScript challenges

Install `nodejs` from official website https://nodejs.org/en/download/ and run following command:

```bash
    npm install
```