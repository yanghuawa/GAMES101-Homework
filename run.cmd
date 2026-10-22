@echo off
setlocal EnableExtensions

set "ROOT=%~dp0"

if "%~1"=="" (
    echo usage: run.cmd ^<hwN^> [args...]
    exit /b 1
)

set "HW=%~1"
shift

set "ARGS="
:collect
if "%~1"=="" goto :run
set "ARGS=%ARGS% %~1"
shift
goto :collect

:run
set "EXE=%ROOT%build\%HW%\%HW%.exe"
if not exist "%EXE%" (
    echo [run] %EXE% not found. Run build.cmd %HW% first.
    exit /b 1
)

pushd "%ROOT%hw\%HW%"
"%EXE%"%ARGS%
set "CODE=%ERRORLEVEL%"
popd

exit /b %CODE%
