import csv
import json
import os

#Creo il dataset in formato CSV
def createCSVDataset(input_file):
    
    output_file = os.path.splitext(input_file)[0] + '.csv'

    try:
        with open(input_file, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            
            if not isinstance(data, list):
                raise ValueError("JSON file does not contain a list of entries.")

            #Definisco i campi basandomi sulle chiavi del primo elemento
            fieldnames = data[0].keys()

            with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)

            print(f"File CSV successfully created: {output_file}")

    #Possibili exceptions
    except FileNotFoundError:
        print(f"The file {input_file} was not found.")
    except json.JSONDecodeError:
        print("Decoding error for JSON file.")
    except Exception as e:
        print(f"There was an error: {e}")