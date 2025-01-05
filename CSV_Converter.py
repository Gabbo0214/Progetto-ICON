import csv
import json

#Crea il dataset in formato CSV
def createCSVDataset():
    with open('restaurantsMeilisearch.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    with open('restaurantList.csv', 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = []
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()


#Funzione che scrive un assiomar nel file kb.pl
def write_fact_to_file(fact, file_path):
    # Verifica se il fatto è già presente
    with open(file_path, 'r', encoding='utf-8') as file:
        existing_content = file.read()

    if fact not in existing_content:
        # Riapri il file in modalità append e scrivi il fatto
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(f"{fact}.\n")


#Funzione che scrive le informazioni dei ristoranti nel file kb.pl
def writeRestaurantInfo(dataSet):
    file_path = "kb.pl"
    with open(file_path, "w", encoding="utf-8") as file:  # Sovrascrivi il file (svuotalo)
        write_fact_to_file(":- encoding(utf8)", file_path)
        for index, row in dataSet.iterrows():
            #remove the ' from the name
            name=name.replace("'", "")
            author=author.replace("'", "")
            prolog_clause = ""
            write_fact_to_file(prolog_clause, file_path)


#Funzione che scrive le informazioni dei cluster nel file kb.pl
def writeClusterInfo(dataSet):
    file_path = "kb.pl"
    #oepn file in append mode
    with open(file_path, "a", encoding="utf-8") as file:  # Sovrascrivi il file (svuotalo)
        for index, row in dataSet.iterrows():
            clusterIndex = row['clusterIndex']
            prolog_clause = f"clustered_restaurant()"
            write_fact_to_file(prolog_clause, file_path)


#Funzione che definisce e testa le regole
def writeRules():
    with open("kb.pl", "a", encoding="utf-8") as file:
        rule=""
        write_fact_to_file(rule, "kb.pl")
    prolog = Prolog()
    prolog.consult("kb.pl")
    clustersIndex=set()
    with open("newDataset.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            clustersIndex.add(row['clusterIndex'])
    clustersIndex = [float(i) for i in clustersIndex]
    for i in clustersIndex:
        print("Cluster: ", i)
        result = list(prolog.query(""))
        for l in result:
            print(l)
        print("\n\n")


#Funzione che estrae le info di un ristorante
def estraiInfo(track_uri):

    return {}