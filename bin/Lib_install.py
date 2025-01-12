import subprocess
import sys
import importlib

#Funzione per installare una libreria
def install(package):  
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

#Verifico se una libreria è installata, altrimenti la installo
def check_and_install_library(libraries):   
    for library in libraries:
        try:
            #Verifico se la libreria è già importabile
            importlib.import_module(library)
            print(f"Libreria '{library}' già installata.")
        except ImportError:
            #Se la libreria non è installata, la installo
            print(f"Libreria '{library}' non trovata. Inizio il download...")
            install(library)

#Funzione per leggere il file requirements.txt e ottenere le librerie
def get_libraries_from_requirements():
    libraries = []
    try:
        with open('bin/requirements.txt', 'r') as file:
            #Aggiungo ogni riga del file come libreria
            libraries = [line.strip() for line in file if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print("Il file 'requirements.txt' non è presente o non è stato trovato.")
    return libraries

def check_and_install_libraries():
    # Ottieni le librerie dal file requirements.txt
    libraries = get_libraries_from_requirements()

    if libraries:
        # Chiamata alla funzione per controllare e installare le librerie
        check_and_install_library(libraries)
        
        
