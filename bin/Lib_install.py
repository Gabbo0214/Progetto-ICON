import subprocess
import sys
import pkg_resources

def install(package):
    """Installa un pacchetto usando pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"Installazione di '{package}' completata.")
    except subprocess.CalledProcessError as e:
        print(f"[❌] Errore durante l'installazione di '{package}': {e}")
    except OSError as e:
        print(f"[❌] Errore di sistema durante l'installazione di '{package}': {e}. Assicurati che pip sia installato.")

def check_and_install_libraries(requirements_file='bin/requirements.txt'):
    """Controlla e installa le librerie da un file requirements.txt."""
    try:
        with open(requirements_file, 'r') as file:
            libraries = [line.strip() for line in file if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print(f"[⚠️] Attenzione: File '{requirements_file}' non trovato. Installazione librerie saltata.")
        return

    if not libraries:
        print("[ℹ️] Il file requirements.txt è vuoto. Nessuna libreria da installare.")
        return

    print("Controllo e installazione delle librerie...\n")
    for library in libraries:
        try:
            pkg_resources.require(library)
            print(f"Libreria '{library}' già installata (o versione compatibile).")

        except pkg_resources.DistributionNotFound:
            print(f"Libreria '{library}' non trovata. Inizio l'installazione...")
            install(library)
        except pkg_resources.VersionConflict as e:
            print(f"[⚠️] Attenzione: Conflitto di versione per '{library}': {e}. Potrebbe essere necessario aggiornare o specificare una versione.")
        except Exception as e:
            print(f"[❌] Errore durante il controllo di '{library}': {e}")

    print("\n[✔️] Controllo e installazione completati.")