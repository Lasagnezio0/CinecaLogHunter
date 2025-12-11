import sys
import shutil
import subprocess
import os
import time
import platform
import glob 
import shlex 
from datetime import datetime

# --- IMPORTIAMO LE LIBRERIE GRAFICHE ---
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.table import Table
    from rich.prompt import Prompt
    from rich.status import Status
    # Proviamo a importare pyfiglet per l'ASCII art
    try:
        import pyfiglet
    except ImportError:
        pyfiglet = None
except ImportError:
    print("ERRORE CRITICO: Esegui 'pip install rich pyfiglet'")
    sys.exit(1)

console = Console()

# --- 1. CONFIGURAZIONE MOTORE ---
def get_search_engine(context_lines=20):
    system_os = platform.system()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    bin_dir = os.path.join(base_dir, "bin")
    
    if system_os == "Windows":
        local_rg_name = "rg.exe"
    else:
        local_rg_name = "rg"
        
    local_rg_path = os.path.join(bin_dir, local_rg_name)
    
    if os.path.exists(local_rg_path):
        if system_os != "Windows":
            try:
                st = os.stat(local_rg_path)
                os.chmod(local_rg_path, st.st_mode | 0o111)
            except Exception: pass
        return [local_rg_path, "-n", f"--context={context_lines}"], f"Portable ({local_rg_name})"

    rg_path = shutil.which("rg")
    if rg_path: return ["rg", "-n", f"--context={context_lines}"], "System Ripgrep"
    
    grep_path = shutil.which("grep")
    if grep_path: return ["grep", "-n", "-B", str(context_lines), "-A", str(context_lines)], "GNU Grep"
    
    return None, None

# --- 2. CORE RICERCA ---
def search_in_file(filepath, search_term, output_folder):
    engine_cmd, engine_name = get_search_engine(context_lines=20)
    if not engine_cmd: return 0, "Motore mancante"

    safe_name = filepath.replace(os.sep, "_").replace(":", "").replace(".", "_")[-30:]
    output_filename = os.path.join(output_folder, f"RES_{safe_name}.txt")
    full_command = engine_cmd + [search_term, filepath]
    match_count = 0
    
    try:
        with open(output_filename, "w", encoding="utf-8") as out_f:
            out_f.write(f"ANALISI: {filepath}\nQUERY: {search_term}\nDATA: {datetime.now()}\n{'='*60}\n\n")
            process = subprocess.Popen(full_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace')
            for line in process.stdout:
                out_f.write(line)
                if search_term in line: match_count += 1
            process.wait()
    except Exception as e: return 0, str(e)
    
    return match_count, "OK"

# --- 3. MAIN ---
def main():
    console.clear()
    _, engine_name = get_search_engine()
    
    # --- ASCII ART ---
    if pyfiglet:
        try:
            # justify="center" centra il testo nella finestra, molto più pro
            ascii_title = pyfiglet.figlet_format("LOG HUNTER", font="ansi_shadow")
        except Exception:
            ascii_title = pyfiglet.figlet_format("LOG HUNTER", font="slant")
            
        console.print(Text(ascii_title, style="bold cyan", justify="center"))
        console.print(f"[white on blue] CINECA EDITION v6.0 [/white on blue] [dim]Motore: {engine_name}[/dim]\n")
    else:
        console.print(Panel(Text(f" CINECA LOG HUNTER v6.0 \n Motore: {engine_name} ", style="bold white on blue"), border_style="blue"))

    if not engine_name:
        console.print("[red]ERRORE: Nessun motore trovato (rg/grep)[/red]")
        return

    # Input
    search_term = Prompt.ask("[bold yellow]Cosa cerco?[/bold yellow]", default="ERROR")
    console.print("[dim]Info: Usa le virgolette per percorsi con spazi[/dim]")
    files_input = Prompt.ask("[bold yellow]Dove (es. *.log)?[/bold yellow]", default="*.log")
    
    # Discovery
    console.print("[dim]Scansione file...[/dim]")
    files_to_scan = []
    
    try:
        raw_patterns = shlex.split(files_input, posix=False)
    except Exception:
        raw_patterns = files_input.split()

    for pat in raw_patterns:
        pat = pat.strip('"').strip("'")
        files_to_scan.extend(glob.glob(pat, recursive=True))
        
    files_to_scan = list(set([f for f in files_to_scan if os.path.isfile(f)]))
    
    if not files_to_scan:
        console.print(f"[red]Nessun file trovato![/red]")
        return

    # --- OUTPUT SETUP CORRETTO ---
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 1. Definiamo la cartella madre
    base_report_dir = "SCANSIONI"
    
    # 2. Definiamo la sottocartella specifica
    out_folder = os.path.join(base_report_dir, f"Report_{ts}")
    
    # 3. Creiamo tutto in un colpo solo (makedirs crea anche i genitori se mancano)
    os.makedirs(out_folder, exist_ok=True)
    # -----------------------------

    # Esecuzione
    table = Table(title=f"Risultati: {search_term}", border_style="cyan")
    table.add_column("File", style="white")
    table.add_column("Match", style="bold green", justify="right")
    
    total = 0
    start = time.time()
    
    with console.status("[bold cyan]Analisi in corso...[/bold cyan]", spinner="simpleDotsScrolling") as status:
        for file in files_to_scan:
            status.update(f"Leggo: {os.path.basename(file)}")
            count, msg = search_in_file(file, search_term, out_folder)
            if msg == "OK":
                total += count
                color = "green" if count > 0 else "dim white"
                table.add_row(os.path.basename(file), f"[{color}]{count}[/{color}]")
            else:
                table.add_row(os.path.basename(file), "[red]Errore[/red]")

    # Riepilogo
    console.print(table)
    console.print(Panel(
        f"Totale Trovati: [bold red]{total}[/bold red]\n"
        f"Tempo: [bold white]{time.time()-start:.2f}s[/bold white]\n"
        f"Cartella: [underline]{out_folder}[/underline]", 
        title="Scansione Completata", border_style="green"
    ))

if __name__ == "__main__":
    main()