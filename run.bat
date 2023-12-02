@echo off
setlocal

set "PYTHON_VERSION=3.11.6"
set "PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-embed-amd64.zip"
set "PYTHON_DIR=python"
set "REQUIREMENTS_FILE=requirements.txt"
set "MAIN_FILE=cctest.py"
set "GET_PIP_URL=https://bootstrap.pypa.io/get-pip.py"

:: Check if Python directory exists
if not exist "%PYTHON_DIR%" (
    echo Python directory not found. Downloading and installing Python...

    :: Download Python
    powershell -Command "Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile python.zip"

    :: Unzip Python
    powershell -Command "Expand-Archive -Path python.zip -DestinationPath %PYTHON_DIR%"

    :: Rename the extracted directory
    for /D %%a in (*Python-%PYTHON_VERSION%-embed-amd64*) do ren "%%a" "%PYTHON_DIR%"

    :: Delete the zip file
    del python.zip

    echo Python installed successfully.
)

:: Activate the Python environment
set "PATH=%CD%\%PYTHON_DIR%;%PATH%"

:: Install pip
if not exist "%PYTHON_DIR%\Scripts\pip.exe" (
    echo Installing pip...

    :: Download get-pip.py
    powershell -Command "Invoke-WebRequest -Uri '%GET_PIP_URL%' -OutFile get-pip.py"

    :: Run get-pip.py
    python get-pip.py

    :: Delete get-pip.py
    del get-pip.py

    echo pip installed successfully.

    :: Read article https://michlstechblog.info/blog/python-install-python-with-pip-on-windows-by-the-embeddable-zip-file/
    timeout /t 2 /nobreak > NUL
    echo %CD%\%PYTHON_DIR% >> %PYTHON_DIR%\python311._pth
    echo %CD%\%PYTHON_DIR%\DLLs >> %PYTHON_DIR%\python311._pth
    echo %CD%\%PYTHON_DIR%\Lib >> %PYTHON_DIR%\python311._pth
    echo %CD%\%PYTHON_DIR%\Lib\plat-win >> %PYTHON_DIR%\python311._pth
    echo %CD%\%PYTHON_DIR%\Lib\site-packages >> %PYTHON_DIR%\python311._pth
    echo %CD% >> %PYTHON_DIR%\python311._pth
)

:: Install dependencies
echo Install dependencies...


:: > %CD%\%PYTHON_DIR%/python311._pth


python -m ensurepip --user
python -m pip install -r "%REQUIREMENTS_FILE%"

:: Run the main file
python -m streamlit run "%MAIN_FILE%"

endlocal