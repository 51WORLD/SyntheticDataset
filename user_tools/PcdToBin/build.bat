if not exist build md build
if not exist pcd_bin md pcd_bin
cd build
cmake ../src -G "Visual Studio 15 2017"

@echo off
if not exist "%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe" ( echo "ERROR: VS2017 not found" )
for /f "tokens=*" %%a in ('"%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe" -property productPath') do set devenv=%%a
"%devenv:~0,-4%.com" .\BinToPcd.sln /build Release
pause
if %ERRORLEVEL% GEQ 1 EXIT /B 1