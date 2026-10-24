@echo off
setlocal
set "MSYS=C:\msys64\mingw64"
set "PATH=%MSYS%\bin;%PATH%"

g++ -std=c++17 -I"%MSYS%\include" "projection_demo.cpp" -o "projection_demo.exe"
if errorlevel 1 exit /b 1

projection_demo.exe
