import csv
import json
import os

def createCSVDataset(input_file):
    """Converto il dataset da JSON a CSV creando un nuovo file."""
    output_file = os.path.splitext(input_file)[0] + '.csv'

    try:
        with open(input_file, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            
            if not isinstance(data, list):
                raise ValueError("Il file JSON non contiene una lista di istanze.")

            # Definisco i campi basandomi sulle chiavi del primo elemento
            fieldnames = data[0].keys()

            with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)

            print(f"File CSV creato con successo: {output_file}")

    # Possibili exceptions
    except FileNotFoundError:
        print(f"Il file {input_file} non è stato trovato.")
    except json.JSONDecodeError:
        print("Errore di codifica del file JSON.")
    except Exception as e:
        print(f"Un errore è stato riscontrato: {e}")