@echo off

python --version 2>NUL | findstr /R "3\.11\.4" >NUL
if %errorlevel% equ 0 (
    echo Python 3.11.4 is installed seems good.
) else (
    echo Python 3.11.4 is not installed Please install it make sure to add it to the patch
    pause
)
ping 127.0.0.1 -n 2 >nul
cls
mkdir data

echo. > data/logs.txt
echo. > data/tokens.txt

pip install requests
cls
pip install colorama
cls
pip install logging
cls
pip install pystyle
cls
pip install tls-client
cls
pip install dtypes
cls

pause
