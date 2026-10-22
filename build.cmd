@echo off
setlocal EnableExtensions

set "ROOT=%~dp0"
set "MSYS=C:\msys64\mingw64"
set "PATH=%MSYS%\bin;%PATH%"

if "%~1"=="" (
    echo usage: build.cmd ^<hwN^>
    exit /b 1
)

set "HW=%~1"
set "SRC=%ROOT%hw\%HW%"
set "OUT=%ROOT%build\%HW%"

if not exist "%SRC%\CMakeLists.txt" (
    echo [build] no such homework: %SRC%
    exit /b 1
)

cmake -S "%SRC%" -B "%OUT%" -G "MinGW Makefiles" -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH="%MSYS%"
if errorlevel 1 exit /b 1

cmake --build "%OUT%" -j 8
if errorlevel 1 exit /b 1

echo.
echo [build] ok: %OUT%\%HW%.exe
