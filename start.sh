#!/bin/bash

echo "=========================================="
echo "      CINECA LOG HUNTER - LINUX SETUP     "
echo "=========================================="

# 1. Pulizia preventiva (se il venv è rotto, lo rifacciamo)
# Scommenta la riga sotto se continua a dare problemi
# rm -rf venv

# 2. Crea il Virtual Environment se non esiste
if [ ! -d "venv" ]; then
    echo "[INFO] Creazione ambiente virtuale..."
    # Se questo fallisce, hai saltato il PASSO 1!
    python3 -m venv venv || { echo "[ERRORE] Impossibile creare venv. Esegui: sudo apt install python3-venv"; exit 1; }
fi

# 3. Installa dipendenze (USANDO IL PIP DEL VENV, NON QUELLO DI SISTEMA)
echo "[INFO] Installazione/Verifica dipendenze..."
./venv/bin/pip install -r requirements.txt

# 4. Permessi al motore portatile
if [ -f "bin/rg" ]; then
    chmod +x bin/rg
fi

# 5. Avvia il programma (USANDO IL PYTHON DEL VENV)
echo ""
echo "[INFO] Avvio Log Hunter..."
echo ""
./venv/bin/python3 main.py