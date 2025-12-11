@echo off
title CINECA Log Hunter - Launcher
cls

echo ==================================================
echo      CINECA LOG HUNTER - SETUP AUTOMATICO
echo ==================================================
echo.

REM 1. Verifica Python
python --version >NUL 2>&1
if errorlevel 1 (
    echo [ERRORE] Python non trovato! Installalo dal Microsoft Store.
    pause
    exit
)

REM 2. Crea ambiente virtuale se manca
if not exist "venv" (
    echo [INFO] Primo avvio: Creazione ambiente virtuale...
    python -m venv venv
)

REM 3. Installa/Aggiorna librerie
echo [INFO] Controllo dipendenze...
.\venv\Scripts\python.exe -m pip install -r requirements.txt >NUL 2>&1

REM 4. Avvia il programma
echo [INFO] Avvio Log Hunter...
echo.
.\venv\Scripts\python.exe main.py

echo.
echo Programma terminato.
pause