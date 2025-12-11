#!/bin/bash

echo "=========================================="
echo "      CINECA LOG HUNTER - LINUX SETUP     "
echo "=========================================="

# 1. Controlla se Python3 è installato
if ! command -v python3 &> /dev/null
then
    echo "[ERRORE] Python3 non trovato. Installalo (es. sudo apt install python3)"
    exit 1
fi

# 2. Crea il Virtual Environment se non esiste
if [ ! -d "venv" ]; then
    echo "[INFO] Creazione ambiente virtuale..."
    python3 -m venv venv
fi

# 3. Attiva venv e installa dipendenze
echo "[INFO] Controllo dipendenze..."
source venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1

# 4. Assicura che il motore portatile sia eseguibile
if [ -f "bin/rg" ]; then
    chmod +x bin/rg
fi

# 5. Avvia il programma
echo "[INFO] Avvio Log Hunter..."
echo ""
python3 main.py