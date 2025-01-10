import subprocess
import sys
import importlib

# Funzione per installare una libreria
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Funzione per verificare se una libreria è installata, altrimenti la installa
def check_and_install_library(libraries):
    for library in libraries:
        try:
            # Verifica se la libreria è già importabile
            importlib.import_module(library)
            print(f"Libreria '{library}' già installata.")
        except ImportError:
            # Se la libreria non è installata, installa
            print(f"Libreria '{library}' non trovata. Installazione in corso...")
            install(library)

# Funzione per leggere il file requirements.txt e ottenere le librerie
def get_libraries_from_requirements():
    libraries = []
    try:
        with open('bin/requirements.txt', 'r') as file:
            # Aggiunge ogni riga del file come una libreria
            libraries = [line.strip() for line in file if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print("File 'requirements.txt' non trovato.")
    return libraries

def check_and_install_libraries():
    # Ottieni le librerie dal file requirements.txt
    libraries = get_libraries_from_requirements()

    if libraries:
        # Chiamata alla funzione per controllare e installare le librerie
        check_and_install_library(libraries)
        
        
