@echo off
echo Testing Air-Piano executable...
echo This will run for 5 seconds then close automatically
echo.

timeout /t 3 /nobreak > nul

start /wait /min cmd /c "dist\Air-Piano.exe & timeout /t 5 /nobreak > nul & taskkill /f /im Air-Piano.exe 2>nul"

echo.
echo Test completed! If you saw camera access or MediaPipe messages, the build is working.
echo.
echo To run Air-Piano normally, use:
echo   - Double-click Air-Piano.exe in the dist folder
echo   - Or run Run-Air-Piano.bat
echo.
pause
