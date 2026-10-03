@echo off
setlocal
cd /d "%~dp0.."
for %%F in (Anlagen.dat Anlagen.classic Anlagen.addon) do (
  if not exist "%~dp0Original_%%F" (
    echo Original backup for %%F is missing.
    pause
    exit /b 1
  )
)
if not exist "%~dp0Original_BGruppen.dat" (
  echo Original backup for BGruppen.dat is missing.
  pause
  exit /b 1
)
for %%F in (Anlagen.dat Anlagen.classic Anlagen.addon) do copy /y "%~dp0Original_%%F" "%%F" >nul || goto :error
copy /y "%~dp0Original_BGruppen.dat" "Data\BGruppen.dat" >nul || goto :error
echo Original Anno 1503 building archives and resident data restored.
pause
exit /b 0
:error
echo Restore failed. Check the game folder and run this file again.
pause
exit /b 1
