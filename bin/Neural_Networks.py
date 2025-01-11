import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Flatten, Reshape
from tensorflow.keras.optimizers import Adam

# Variabili globali per dati precaricati
autoencoder = None
rating_matrix = None
restaurants = None

def train_autoencoder(data_path_restaurants='dataset/restaurantList.json', data_path_ratings='dataset/userRatings.json', epochs=50, batch_size=32):
    global autoencoder, rating_matrix, restaurants

    # 1. Carico i dataset
    restaurants = pd.read_json(data_path_restaurants)
    ratings = pd.read_json(data_path_ratings)

    # 2. Preprocessing: creo una matrice di ristoranti e recensioni
    ratings['restaurant_id'] = ratings['restaurant_id'].astype(int)
    user_ids = ratings['user_id'].astype('category').cat.codes
    restaurant_ids = ratings['restaurant_id'].astype('category').cat.codes

    ratings['user_id_mapped'] = user_ids
    ratings['restaurant_id_mapped'] = restaurant_ids

    num_users = user_ids.nunique()
    num_restaurants = restaurant_ids.nunique()

    rating_matrix = np.zeros((num_users, num_restaurants))
    for row in ratings.itertuples():
        rating_matrix[row.user_id_mapped, row.restaurant_id_mapped] = row.rating

    # 3. Divido i dati in allenamento e test
    train_data, test_data = train_test_split(rating_matrix, test_size=0.2, random_state=42)

    # 4. Definisco il modello autoencoder
    input_layer = Input(shape=(num_restaurants,))
    encoded = Dense(64, activation='relu')(input_layer)
    encoded = Dense(32, activation='relu')(encoded)

    decoded = Dense(64, activation='relu')(encoded)
    decoded = Dense(num_restaurants, activation='linear')(decoded)

    autoencoder = Model(input_layer, decoded)

    # 5. Compilo e alleno il modello
    autoencoder.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')

    # Normalizzazione dei voti
    train_data_norm = train_data / np.max(train_data)
    test_data_norm = test_data / np.max(test_data)

    autoencoder.fit(
        train_data_norm,
        train_data_norm,
        epochs=epochs,
        batch_size=batch_size,
        validation_data=(test_data_norm, test_data_norm),
        shuffle=True
    )

def get_recommendations(user_id, top_n=10):
    
    global autoencoder, rating_matrix, restaurants
    
    #Controllo che tutto sia inizializzato correttamente
    if autoencoder is None or rating_matrix is None or restaurants is None:
        raise ValueError("Autoencoder model and data must be loaded first. Call train_autoencoder() before using get_recommendations().")
    
    #Estraggo voti e ristoranti e normalizzo i voti
    user_ratings = rating_matrix[user_id].reshape(1, -1)
    user_ratings_norm = user_ratings / np.max(rating_matrix)

    #Seleziono tramite l'autoencoder i ristoranti predetti, e li elenco in ordine decrescente per i primi 10
    predicted_ratings = autoencoder.predict(user_ratings_norm)
    recommended_restaurants_ids = (-predicted_ratings).argsort()[0][:top_n]

    #Filtro i ristoranti consigliati e quelli già piaciuti
    recommended_restaurants = restaurants[restaurants['id'].isin(recommended_restaurants_ids)]
    liked_restaurants_ids = np.where(rating_matrix[user_id] >= 4)[0]
    liked_restaurants = restaurants[restaurants['id'].isin(liked_restaurants_ids)].head(3)

    #Stampa dei dati richiesti, ovvero ristoranti piaciuti e consigliati
    print("Based on your liking for these restaurants:")
    for _, row in liked_restaurants.iterrows():
        print(f"- {row['name']}")
    
    print("\nWe recommend:")
    for idx, (_, row) in enumerate(recommended_restaurants.iterrows(), start=1):
        print(f"{idx}. {row['name']}")