@echo off
setlocal
set "MSYS=C:\msys64\mingw64"
set "PATH=%MSYS%\bin;%PATH%"

g++ -std=c++17 -I"%MSYS%\include" "eigen_basics.cpp" -o "eigen_basics.exe"
if errorlevel 1 exit /b 1

eigen_basics.exe
