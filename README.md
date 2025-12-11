```
██╗      ██████╗  ██████╗    ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗ 
██║     ██╔═══██╗██╔════╝    ██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
██║     ██║   ██║██║  ███╗   ███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝
██║     ██║   ██║██║   ██║   ██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗
███████╗╚██████╔╝╚██████╔╝   ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║
╚══════╝ ╚═════╝  ╚═════╝    ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
```

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

## Installazione

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

Una volta avviato, il programma ti guiderà passo passo attraverso un'interfaccia interattiva.

### Fase 1: Cosa Cercare?

Inserisci la stringa da ricercare nei log:
* `ERROR` - ricerca stringhe esatte
* `CRITICAL` - case-insensitive 

### Fase 2: Dove Cercare?

Specifica il percorso target con questi pattern:

* **File singolo:** `server.log`
* **Tutti i log nella cartella:** `*.log`
* **Ricerca ricorsiva profonda:** `**/*.log`
* **Filtri specifici:** `logs/**/*error*.log`

### Fase 3: Risultati

Il tool genera un report strutturato:

```
[Analisi in corso...] ⏳
Leggo: server_nodo1.log ...
Leggo: server_nodo2.log ...

┌─────────────────────────┬────────────┐
│ File                    │   Match    │
├─────────────────────────┼────────────┤
│ server_nodo1.log        │     45     │
│ error_dump.log          │   1200     │
└─────────────────────────┴────────────┘
```

I risultati vengono salvati automaticamente in `SCANSIONI/Report_TIMESTAMP/` per una consultazione successiva.

---

## Architettura Tecnica

Il progetto è costruito su un'architettura **ibrida e modulare**:

### Componenti Principali

| Componente | Tecnologia | Ruolo |
|-----------|-----------|-------|
| **Frontend** | Python 3 + Rich | Logica di business, interfaccia TUI, gestione percorsi |
| **Search Engine** | Ripgrep (Rust) | Motore I/O ad altissime performance |
| **Fallback** | grep (sistema) | Backup per ambienti senza binari |
| **Visualizzazione** | Rich + Pyfiglet | Output colorato e formattato |

### Flusso di Esecuzione

1. **Parsing Input:** L'interfaccia Python elabora pattern di ricerca e percorsi usando `shlex` e `glob`
2. **Selezione Engine:** 
   - Windows → esegue `bin/rg.exe`
   - Linux → esegue `bin/rg`
3. **Fallback Logic:** Se i binari portatili non sono disponibili, ricade su `grep` di sistema
4. **Aggregazione:** I risultati vengono raccolti e formattati per la visualizzazione

---

## Autori

Sviluppato da **Alessandro** ed **Enrico** presso **CINECA** nel percorso PCTO.