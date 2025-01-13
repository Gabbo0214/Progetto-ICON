import csv
from collections import defaultdict
import math
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import string
from sklearn.model_selection import KFold
from sklearn.metrics import precision_score, recall_score, f1_score

# Scarica le risorse NLTK necessarie
try:
    nltk.data.find('corpora/stopwords')
    nltk.data.find('wordnet')
    nltk.data.find('punkt')
except LookupError:
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('punkt')

# Inizializzazione del lemmatizzatore e delle stop words
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    """Esegue il preprocessing del testo."""
    # Riduco tutto in minuscolo, rimuovo le stop words e "tokenizzo" le parole
    # Infine, applico la lemmatizzazione
    words = word_tokenize(text.lower())
    processed_words = [
        word for word in words
        if word not in stop_words and word.isalpha() and word not in string.punctuation
    ]
    processed_words = [lemmatizer.lemmatize(word) for word in processed_words]
    return processed_words

def load_data_from_csv(csv_file):
    """Carica i dati da un file CSV."""
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = list(reader)
        return data
    except FileNotFoundError:
        print(f"[❌] Errore: File non trovato: {csv_file}")
        return None

def prepare_data(data):
    """Prepara i dati per il classificatore Naive Bayes."""
    # Creo un dizionario di dizionari.
    # Al primo livello mappo le categorie con le parole contenute 
    # Al secondo livello il conteggio delle parole
    word_counts = defaultdict(lambda: defaultdict(int))
    category_counts = defaultdict(int)
    for row in data:
      if 'description' in row and 'categories' in row:
        category = row['categories']
        description = row['description']
        category_counts[category] += 1
        words = preprocess_text(description)
        for word in words:
            word_counts[category][word] += 1
    return word_counts, category_counts

def predict_category(description, word_counts, category_counts):
    """Predice la categoria di un ristorante data la sua descrizione."""
    # Assegno la descrizione, faccio il conto di tutti gli elementi
    # (ristoranti) e creo un dizionario di punteggi. Ad ogni categoria
    # assegno un punteggio basato su probabilità in base alle parole
    words = preprocess_text(description)
    total_docs = sum(category_counts.values())
    scores = {}
    for category in category_counts:
        score = math.log(category_counts[category] / total_docs)
        for word in words:
            # Uso dello smoothing di laplace per non azzerare il punteggio con parole rare
            word_probability = (word_counts[category][word] + 0.1) / (sum(word_counts[category].values()) + len(word_counts[category]))
            score += math.log(word_probability)
        scores[category] = score
    return max(scores, key=scores.get)

def evaluate_classifier(data, word_counts, category_counts, k=4):
    """
    Valuta il classificatore usando K-fold cross-validation e calcola precision, recall e F1-score.
    """
    # Divido in 4 pieghe mescolate in base a un seed i dati
    kf = KFold(n_splits=k, shuffle=True, random_state=42)
    true_labels = []
    predicted_labels = []

    # Testing del modello. passando per gli indici elencati nei fold, si raccolgono
    # le descrizioni e le categorie effettive, e si mettono in liste i label (categorie)
    # predette (tramite la funzione precedente) e reali al fine di misurare l'accuratezza.
    for train_index, test_index in kf.split(data):
        test_data = [data[i] for i in test_index]
        for row in test_data:
          if 'description' in row and 'categories' in row:
            description = row['description']
            true_category = row['categories']
            predicted_category = predict_category(description, word_counts, category_counts)
            true_labels.append(true_category)
            predicted_labels.append(predicted_category)

    # Calcolo le metriche di valutazione del classificatore
    precision = precision_score(true_labels, predicted_labels, average='weighted', zero_division=0) # Quante volte le predizioni erano esatte
    recall = recall_score(true_labels, predicted_labels, average='weighted', zero_division=0) # Quante volte la categoria più probabile è stata individuata
    f1 = f1_score(true_labels, predicted_labels, average='weighted', zero_division=0) # Una media di recall e precision

    return precision, recall, f1

def show_restaurants_by_category(data, word_counts, category_counts, selected_category):
    """
    Mostra i ristoranti per categoria, filtrando quelli già presenti nelle recensioni dell'utente.
    """
    print(f"\n[️👨‍🍳 ] Ecco a te i ristoranti {selected_category}:\n")
    # Mostra i ristoranti della categoria richiesta dall'utente usando le predizioni del programma
    for row in data:
      if 'description' in row and 'categories' in row and 'name' in row:
        description = row['description']
        name = row['name']
        predicted_category = predict_category(description, word_counts, category_counts)
        if predicted_category == selected_category:
            print(f"- {name}")

def supervised_learning(csv_file='dataset/restaurantList.csv'):
    """Funzione principale per il Supervised Learning."""
    print("\n[📊 ] Avvio del Supervised Learning per la classificazione dei ristoranti...")

    data = load_data_from_csv(csv_file)
    if data is None:
        return

    word_counts, category_counts = prepare_data(data)
    if not category_counts:
      print("[❌] Nessuna categoria trovata. Controlla il dataset.")
      return

    # Stampo le valutazioni calcolate con la funzione presente sopra
    precision, recall, f1 = evaluate_classifier(data, word_counts, category_counts)
    print(f"\n[] Valutazione del classificatore:")
    print(f"Precisione: {precision * 100:.2f}%")
    print(f"Recall: {recall * 100:.2f}%")
    print(f"F1-score: {f1 * 100:.2f}%")

    # Raccolgo in ordine alfabetico le categorie uniche trovate, le stampo in ordine e offro
    # la selezione all'utente per la stampa di ogni ristorante appartenente alla stessa.
    unique_categories = sorted(set(row['categories'] for row in data if 'categories' in row))
    while True:
        print("\n[️📃] Categorie disponibili:")
        for i, category in enumerate(unique_categories, 1):
            print(f"{i}. {category}")
        try:
            category_choice = int(input("[‍📑] Seleziona una categoria con un numero (0 per uscire): "))
            if category_choice == 0:
                break
            selected_category = unique_categories[category_choice - 1]
            show_restaurants_by_category(data, word_counts, category_counts, selected_category)
        except (ValueError, IndexError):
            print("[❌] Scelta non valida. Riprova.")

    print("\n[✔️ ] Supervised Learning completato.")