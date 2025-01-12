import subprocess
import sys
import importlib
import nltk 

#Funzione per installare una libreria
def install(package):  
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

#Funzione di controllo per installare pacchetti nltk
def download_if_missing(resource):
    try:
        nltk.data.find(resource)
    except LookupError:
        print(f"Installing {resource}...")
        nltk.download(resource)

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
    
    choice = input ("Vuoi installare le librerie necessarie? ATTENZIONE: senza di esse il programma non funzionerà: ")
    if choice in ["yes", "y", "Y", "Yes", "Si", "si", "s", "S"]:
        # Ottieni le librerie dal file requirements.txt
        libraries = get_libraries_from_requirements()

        if libraries:
            # Chiamata alla funzione per controllare e installare le librerie
            check_and_install_library(libraries)

        #Scarica risorse necessarie per nltk solo se non già presenti
        download_if_missing('stopwords')
        download_if_missing('punkt_tab')
        download_if_missing('wordnet')
        download_if_missing('omw-1.4') 
        
