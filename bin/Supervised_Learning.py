import csv
from collections import defaultdict
from CSV_Converter import createCSVDataset
import math
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


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

# Funzione di preprocessing avanzato
def preprocess_text(text):
    # Tokenizza il testo
    words = word_tokenize(text.lower())  # Trasforma in minuscolo e tokenizza
    # Rimuovi le stopwords e lemmatizza le parole
    processed_words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words and word.isalpha()]
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
        words = preprocess_text(description)  # Preprocessing avanzato
        for word in words:
            word_counts[category][word] += 1
    
    return word_counts, category_counts

# Funzione per calcolare le probabilità
def predict_category(description, word_counts, category_counts):
    words = preprocess_text(description)  # Preprocessing avanzato
    total_docs = sum(category_counts.values())
    
    scores = {}
    for category in category_counts:
        # Calcolo probabilità della categoria
        score = math.log(category_counts[category] / total_docs)
        for word in words:
            # Laplace smoothing
            word_probability = (word_counts[category][word] + 1) / \
                               (sum(word_counts[category].values()) + len(word_counts[category]))
            score += math.log(word_probability)
        scores[category] = score
    
    # Restituisce la categoria con il punteggio più alto
    return max(scores, key=scores.get)

# Esegui il modello
def Supervised_learning():
     
    createCSVDataset("dataset/restaurantsMeilisearch.json")
    createCSVDataset("dataset/user_ratings.json")
    csv_file = 'dataset/restaurantsMeilisearch.csv'  # Nome del file CSV
    descriptions, categories = load_data_from_csv(csv_file)
    
    # Divide i dati in training e test set (80% training, 20% test)
    split_index = int(0.8 * len(descriptions))
    train_descriptions = descriptions[:split_index]
    train_categories = categories[:split_index]
    test_descriptions = descriptions[split_index:]
    test_categories = categories[split_index:]
    
    # Prepara i dati
    word_counts, category_counts = prepare_data(train_descriptions, train_categories)
    
    # Valutazione sul test set
    correct = 0
    for description, true_category in zip(test_descriptions, test_categories):
        predicted_category = predict_category(description, word_counts, category_counts)
        print(f"Descrizione: {description}")
        print(f"Categoria Predetta: {predicted_category}, Categoria Reale: {true_category}\n")
        if predicted_category == true_category:
            correct += 1
    
    # Accuratezza
    accuracy = correct / len(test_descriptions)
    print(f"Accuratezza: {accuracy * 100:.2f}%")