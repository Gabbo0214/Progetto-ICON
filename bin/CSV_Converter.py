import csv
import json
import os

# Crea il dataset in formato CSV
def createCSVDataset(input_file):
    
    output_file = os.path.splitext(input_file)[0] + '.csv'
    
    columns_to_exclude = ['picture', 'picture_author', 'picture_author_profile_link']

    try:
        with open(input_file, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            
            if not isinstance(data, list):
                raise ValueError("Il file JSON non contiene una lista di oggetti.")
            
            # Rimuovi le colonne specificate da ogni elemento
            for entry in data:
                for col in columns_to_exclude:
                    if col in entry:
                        del entry[col]

            # Definisci i campi basandoti sulle chiavi del primo elemento
            fieldnames = data[0].keys()

            with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)

            print(f"File CSV creato con successo: {output_file}")

    except FileNotFoundError:
        print(f"Il file {input_file} non è stato trovato.")
    except json.JSONDecodeError:
        print("Errore nel decodificare il file JSON.")
    except Exception as e:
        print(f"Si è verificato un errore: {e}")