@echo off
setlocal

set "MAIN_FILE=cctest.py"

:: Run the main file
python -m streamlit run "%MAIN_FILE%"

endlocal