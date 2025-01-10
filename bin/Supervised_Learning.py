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
        print(f"Scaricando {resource}...")
        nltk.download(resource)

# Scarica risorse necessarie per nltk solo se non già presenti
download_if_missing('stopwords')
download_if_missing('punkt')
download_if_missing('punkt_tab')
download_if_missing('wordnet')
download_if_missing('omw-1.4')

# Inizializza il lemmatizzatore e la lista di stopwords
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Funzione di preprocessing avanzato con rimozione della punteggiatura
def preprocess_text(text):
    # Tokenizza il testo, trasforma tutto in minuscolo
    words = word_tokenize(text.lower())
    
    # Rimuovi punteggiatura e stopwords
    processed_words = [
        word for word in words 
        if word not in stop_words and word.isalpha() and word not in string.punctuation
    ]
    
    # Applica il lemmatizzatore
    processed_words = [lemmatizer.lemmatize(word) for word in processed_words]
    
    return processed_words

# Carica i dati dal file CSV
def load_data_from_csv(csv_file):
    descriptions = []
    categories = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            descriptions.append(row['description'])
            categories.append(row['categories'])
    return descriptions, categories

# Prepara i dati per Naive Bayes
def prepare_data(descriptions, categories):
    word_counts = defaultdict(lambda: defaultdict(int))
    category_counts = defaultdict(int)
    
    for description, category in zip(descriptions, categories):
        category_counts[category] += 1
        words = preprocess_text(description)
        for word in words:
            word_counts[category][word] += 1
    
    return word_counts, category_counts

# Funzione per calcolare le probabilità
def predict_category(description, word_counts, category_counts):
    words = preprocess_text(description)
    total_docs = sum(category_counts.values())
    
    scores = {}
    for category in category_counts:
        # Calcolo probabilità della categoria
        score = math.log(category_counts[category] / total_docs)
        for word in words:
            # Laplace smoothing
            word_probability = (word_counts[category][word] + 0.1) / \
                               (sum(word_counts[category].values()) + len(word_counts[category]))
            score += math.log(word_probability)
        scores[category] = score
    
    # Restituisce la categoria con il punteggio più alto
    return max(scores, key=scores.get)

# Esegui il modello con Cross Validation
def Supervised_learning():
    createCSVDataset("dataset/restaurantsList.json")
    createCSVDataset("dataset/user_ratings.json")
    csv_file = 'dataset/restaurantsList.csv'
    descriptions, categories = load_data_from_csv(csv_file)
    
    # Imposta il numero di fold per la cross-validation
    k = 4
    kf = KFold(n_splits=k)
    
    total_correct = 0  # Conta totale delle previsioni corrette
    total_test_samples = 0  # Conta totale dei campioni nel test set
    
    # Esegui la cross-validation
    for train_index, test_index in kf.split(descriptions):
        # Dividi i dati in training e test set per questo fold
        train_descriptions = [descriptions[i] for i in train_index]
        train_categories = [categories[i] for i in train_index]
        test_descriptions = [descriptions[i] for i in test_index]
        test_categories = [categories[i] for i in test_index]
        
        # Prepara i dati
        word_counts, category_counts = prepare_data(train_descriptions, train_categories)
        
        # Valutazione sul test set
        for description, true_category in zip(test_descriptions, test_categories):
            predicted_category = predict_category(description, word_counts, category_counts)
            
            # Stampa la categoria predetta e quella reale
            print(f"Descrizione: {description}")
            print(f"Categoria Predetta: {predicted_category}, Categoria Reale: {true_category}\n")
            
            if predicted_category == true_category:
                total_correct += 1
            total_test_samples += 1
    
    # Calcola l'accuratezza totale
    total_accuracy = total_correct / total_test_samples
    
    # Stampa l'accuratezza totale
    print(f"Accuratezza totale: {total_accuracy * 100:.2f}%")