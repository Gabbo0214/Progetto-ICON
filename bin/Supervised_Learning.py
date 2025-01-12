import csv
from collections import defaultdict
from CSV_Converter import createCSVDataset
import math
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import string
from sklearn.model_selection import KFold

def download_if_missing(resource):
    try:
        nltk.data.find(resource)
    except LookupError:
        print(f"Installing {resource}...")
        nltk.download(resource)

#Scarica risorse necessarie per nltk solo se non già presenti
download_if_missing('stopwords')
download_if_missing('punkt_tab')
download_if_missing('wordnet')
download_if_missing('omw-1.4')

#Inizializza il lemmatizzatore e la lista di stopwords
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

#Funzione di preprocessing avanzato con rimozione della punteggiatura
def preprocess_text(text):
    #Tokenizza il testo, trasforma tutto in minuscolo
    words = word_tokenize(text.lower())
    
    #Rimuovi punteggiatura e stopwords
    processed_words = [
        word for word in words 
        if word not in stop_words and word.isalpha() and word not in string.punctuation
    ]
    
    #Applica il lemmatizzatore
    processed_words = [lemmatizer.lemmatize(word) for word in processed_words]
    
    return processed_words

#Carica i dati dal file CSV
def load_data_from_csv(csv_file):
    names = [] 
    descriptions = []  
    categories = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            names.append(row['name']) 
            descriptions.append(row['description'])
            categories.append(row['categories'])
    return names, descriptions, categories

#Prepara i dati per Naive Bayes
def prepare_data(descriptions, categories):
    word_counts = defaultdict(lambda: defaultdict(int))
    category_counts = defaultdict(int)
    
    for description, category in zip(descriptions, categories):
        category_counts[category] += 1
        words = preprocess_text(description)
        for word in words:
            word_counts[category][word] += 1
    
    return word_counts, category_counts

#Funzione per calcolare le probabilità
def predict_category(description, word_counts, category_counts):
    words = preprocess_text(description)
    total_docs = sum(category_counts.values())
    
    scores = {}
    for category in category_counts:
        #Calcolo probabilità della categoria
        score = math.log(category_counts[category] / total_docs)
        for word in words:
            #Laplace smoothing
            word_probability = (word_counts[category][word] + 0.1) / \
                               (sum(word_counts[category].values()) + len(word_counts[category]))
            score += math.log(word_probability)
        scores[category] = score
    
    #Restituisce la categoria con il punteggio più alto
    return max(scores, key=scores.get)

#Eseguo il modello di apprendimento controllato
def supervised_learning():
    createCSVDataset("dataset/restaurantList.json")
    createCSVDataset("dataset/userRatings.json")
    csv_file = 'dataset/restaurantList.csv'
    names, descriptions, categories = load_data_from_csv(csv_file)
    
    #Preparo i dati per l'allenamento
    word_counts, category_counts = prepare_data(descriptions, categories)
    
    #Eseguo la cross-validation e calcolo l'accuratezza
    k = 4
    kf = KFold(n_splits=k)
    
    total_correct = 0
    total_test_samples = 0 
    
    for train_index, test_index in kf.split(descriptions):
        #Divido i dati in training e test set per questo fold
        train_descriptions = [descriptions[i] for i in train_index]
        train_categories = [categories[i] for i in train_index]
        test_descriptions = [descriptions[i] for i in test_index]
        test_categories = [categories[i] for i in test_index]
        
        #Valutazione sul test set
        for description, true_category in zip(test_descriptions, test_categories):
            predicted_category = predict_category(description, word_counts, category_counts)
            if predicted_category == true_category:
                total_correct += 1
            total_test_samples += 1
    
    #Calcolo e stampo l'accuratezza
    total_accuracy = total_correct / total_test_samples
    print(f"Accuratezza totale: {total_accuracy * 100:.2f}%")
    print("\n[✔️ ] Supervised Learning completato.")
    print("\n[🤖] La nostra intelligenza artificiale ha organizzato i ristoranti per te.")
    
    #Stampo le categorie e richiedo la selezione di una di esse
    show_categories(names, descriptions, categories, word_counts, category_counts)

#Funzione per stampare le categorie uniche
def show_categories(names, descriptions, categories, word_counts, category_counts):
    unique_categories = sorted(set(categories))  # Ordino le categorie alfabeticamente
    print("\n[🍽️ ]Categorie disponibili:")
    for i, category in enumerate(unique_categories, 1):
        print(f"{i}. {category}")
    
    category_choice = int(input("[👨‍🍳]Seleziona una categoria con un numero: "))
    selected_category = unique_categories[category_choice - 1]
    
    #Chiamo la funzione per mostrare i ristoranti in base alla categoria selezionata
    show_restaurants_by_category(selected_category, names, descriptions, categories, word_counts, category_counts)

#Funzione per mostrare i ristoranti per categoria (sia in allenamento che in test)
def show_restaurants_by_category(selected_category, names, descriptions, categories, word_counts, category_counts):
    k = 4
    kf = KFold(n_splits=k)
    
    print(f"\n[🍽️ ]Ecco a te i ristoranti {selected_category}:\n")
    
    # Lista per tenere traccia dei ristoranti già stampati
    printed_restaurants = set()
    
    for train_index, test_index in kf.split(descriptions):
        #Seleziono i dati di allenamento e test per questo fold
        train_names = [names[i] for i in train_index]  
        train_descriptions = [descriptions[i] for i in train_index]
        train_categories = [categories[i] for i in train_index]
        test_names = [names[i] for i in test_index]
        test_descriptions = [descriptions[i] for i in test_index]
        test_categories = [categories[i] for i in test_index]
        
        #Stampo i ristoranti con la categoria effettiva nel training set
        for name, category in zip(train_names, train_categories):
            if category == selected_category and name not in printed_restaurants:
                print(f"Ristorante: {name}") 
                printed_restaurants.add(name)
        
        #Stampo i ristoranti con la categoria predetta nel test set
        for name, description, category in zip(test_names, test_descriptions, test_categories):
            predicted_category = predict_category(description, word_counts, category_counts)
            if predicted_category == selected_category and name not in printed_restaurants:
                print(f"Ristorante: {name}")
                printed_restaurants.add(name)