@echo off

python --version | findstr /C:"Python 3.11" >nul
IF %ERRORLEVEL% NEQ 0 (
    echo Error: please install Python 3.11.
    echo If it is already installed, insert the bin path into the PATH variable.
    exit /b 1
)

IF NOT EXIST venv (
    echo I'm creating a virual environment just for you...
    echo It can takes few minutes, please wait
    echo If this window closes at the end of the process, please reopen it and enjoy!
    python -m venv venv

    venv\Scripts\activate

    pip install -r requirements.txt

    deactivate
)

call .\venv\Scripts\activate.bat
python .\main.py
deactivate