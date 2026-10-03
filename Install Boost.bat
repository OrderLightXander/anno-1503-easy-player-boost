@echo off
setlocal
cd /d "%~dp0.."
if not exist "Anno1503.exe" (
  echo Keep this mod folder directly inside the Anno 1503 install folder, beside Anno1503.exe.
  pause
  exit /b 1
)
for %%F in (Anlagen.dat Anlagen.classic Anlagen.addon) do (
  if not exist "%%F" (
    echo Missing game archive %%F.
    pause
    exit /b 1
  )
  if not exist "%~dp0Original_%%F" copy /y "%%F" "%~dp0Original_%%F" >nul || goto :error
)
if not exist "Data\BGruppen.dat" (
  echo Missing Data\BGruppen.dat.
  pause
  exit /b 1
)
if not exist "%~dp0Original_BGruppen.dat" copy /y "Data\BGruppen.dat" "%~dp0Original_BGruppen.dat" >nul || goto :error
if not exist "%~dp0build_mod.py" (
  echo The mod builder is missing.
  pause
  exit /b 1
)
python "%~dp0build_mod.py" || goto :error
for %%F in (Anlagen.dat Anlagen.classic Anlagen.addon) do (
  if not exist "%~dp0%%F" (
    echo Modded archive %%F is missing.
    pause
    exit /b 1
  )
)
copy /y "%~dp0Anlagen.dat" "Anlagen.dat" >nul || goto :error
copy /y "%~dp0Anlagen.classic" "Anlagen.classic" >nul || goto :error
copy /y "%~dp0Anlagen.addon" "Anlagen.addon" >nul || goto :error
copy /y "%~dp0BGruppen.dat" "Data\BGruppen.dat" >nul || goto :error
echo Anno 1503 Easy Player Boost installed.
echo Production cycles are up to 4x faster, coverage is expanded, and citizens grow faster.
echo Run "Restore Original Files.bat" to undo these changes.
pause
exit /b 0
:error
echo Installation failed. Run "Restore Original Files.bat" to restore all original game data.
pause
exit /b 1
