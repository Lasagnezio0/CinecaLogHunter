██╗      ██████╗  ██████╗     ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗   
██║     ██╔═══██╗██╔════╝     ██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗  
██║     ██║   ██║██║  ███╗    ███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝  
██║     ██║   ██║██║   ██║    ██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗  
███████╗╚██████╔╝╚██████╔╝    ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║  
╚══════╝ ╚═════╝  ╚═════╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝  
                                                                                    

# CINECA Log Hunter

> **High-Performance Log Analysis Tool**  
> Sviluppato durante il percorso PCTO presso CINECA.

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey)
![Engine](https://img.shields.io/badge/Engine-Ripgrep%20(Rust)-orange)

**CINECA Log Hunter** è uno strumento CLI (Command Line Interface) avanzato per la ricerca rapida di stringhe e pattern all'interno di file di log di grandi dimensioni (Gigabyte/Terabyte).

Progettato per essere **portabile** e **performante**, combina la flessibilità di Python (per l'interfaccia utente) con la velocità grezza di `ripgrep` (motore scritto in Rust) per l'elaborazione dei dati.

---

## Caratteristiche Principali

* **Velocità Estrema:** Utilizza un motore ibrido. L'interfaccia è in Python, ma la ricerca I/O è delegata a binari precompilati di `ripgrep` (inclusi nel progetto), garantendo performance fino a 10x rispetto alla ricerca standard.
* **Zero Dependencies (Portable):** Funziona immediatamente su Windows e Linux senza dover installare software esterni. I motori di ricerca sono inclusi nella cartella `bin/`.
* **Interfaccia Grafica TUI:** Utilizza la libreria `rich` per offrire output colorati, barre di caricamento, tabelle riassuntive e titoli in ASCII Art.
* **Ricerca Ricorsiva:** Supporta il globbing avanzato (es. `**/*.log`) per cercare automaticamente in tutte le sottocartelle nidificate.
* **Reporting Organizzato:** I risultati non vengono sovrascritti ma salvati in cartelle `SCANSIONI/Report_TIMESTAMP` per mantenere uno storico pulito.
* **Setup Automatico:** Script di avvio intelligenti (`.bat` e `.sh`) che configurano l'ambiente virtuale e le dipendenze al primo avvio.

---

## 📦 Installazione

Non serve installare nulla manualmente. Clona il repository ed esegui lo script di avvio per il tuo sistema operativo.

### Windows

Basta fare **doppio click** sul file:

Per **start.sh**:

### Linux (Debian/Ubuntu/Kali)

Apri il terminale nella cartella del progetto:

#### 1. Rendi eseguibile lo script (solo la prima volta)
chmod +x start.sh

#### 2. Avvia il tool
./start.sh

#### Assicurati di avere il pacchetto necessario:
sudo apt install python3-venv

## Utilizzo

Una volta avviato, il programma ti guiderà passo passo:

Cosa cercare: Inserisci la stringa o il pattern (es. ERROR, CRITICAL, Exception).

### Dove cercare:

* **File singolo:** server.log

* **Tutti i log nella cartella:** *.log

* **Tutti i log anche nelle sottocartelle:** **/*.log

### Esempio di output:
[Analisi in corso...]  
Leggo: server_nodo1.log ...  
Leggo: server_nodo2.log ...  
  
+-------------------------------------+  
| File              | Match           |  
+-------------------------------------+  
| server_nodo1.log  | 45              |  
| error_dump.log    | 1200            |  
+-------------------------------------+  
  
## Architettura Tecnica

Il progetto segue un approccio **Clean & Portable**:

Core: Python 3 gestisce la logica di business, l'input utente e la gestione dei percorsi (shlex, glob).
Engine:

#### 1. Su Windows, viene eseguito *bin/rg.exe*.

#### 2. Su Linux, viene eseguito *bin/rg*.

**Se i binari portatili falliscono, il sistema cerca grep installato nel sistema come fallback**.

Data Visualization: Librerie rich e pyfiglet per la UX.

## Autore

Sviluppato da Alessandro ed Enrico per progetto PCTO CINECA.