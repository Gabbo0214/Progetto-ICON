import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.optimizers import Adam

autoencoder = None
rating_matrix = None
restaurants_df = None

def train_autoencoder(data_path_restaurants='dataset/restaurantList.json',
                      data_path_ratings='dataset/userRatings.json',
                      epochs=50, batch_size=32):
    """
    Allena un autoencoder per il sistema di raccomandazione.

    Args:
        data_path_restaurants (str): Path al file JSON dei ristoranti.
        data_path_ratings (str): Path al file JSON delle recensioni.
        epochs (int): Numero di epoche di allenamento.
        batch_size (int): Dimensione del batch per l'allenamento.
    """
    global autoencoder, rating_matrix, restaurants_df

    try:
        restaurants_df = pd.read_json(data_path_restaurants)
        ratings = pd.read_json(data_path_ratings)
    except FileNotFoundError:
        print(f"\n[❌] Errore: Uno o entrambi i file non trovati: {data_path_restaurants}, {data_path_ratings}")
        return

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

    train_data, test_data = train_test_split(rating_matrix, test_size=0.2, random_state=42)
    
    input_layer = Input(shape=(num_restaurants,))

    encoded = Dense(64, activation='relu')(input_layer)
    encoded = Dense(32, activation='relu')(encoded)

    decoded = Dense(64, activation='relu')(encoded)
    decoded = Dense(num_restaurants, activation='linear')(decoded)

    autoencoder = Model(input_layer, decoded)

    autoencoder.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')

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
    """
    Genera raccomandazioni per un dato utente.

    Args:
        user_id (int): ID dell'utente per cui generare le raccomandazioni.
        top_n (int): Numero di raccomandazioni da restituire.
    """
    global autoencoder, rating_matrix, restaurants_df

    if autoencoder is None or rating_matrix is None or restaurants_df is None:
        print("\n[❌] Errore: Il modello non è stato allenato. Eseguire train_autoencoder() prima di ottenere raccomandazioni.")
        return

    try:
        user_ratings = rating_matrix[user_id].reshape(1, -1)
    except IndexError:
        print(f"\n[❌] Errore: ID utente {user_id} non valido.")
        return

    # Normalizzo le valutazioni dell'utente
    max_rating = np.max(rating_matrix)
    user_ratings_norm = user_ratings / max_rating if max_rating > 0 else user_ratings

    # Predizione delle valutazioni per tutti i ristoranti.
    predicted_ratings = autoencoder.predict(user_ratings_norm)
    # Ottengo gli ID dei ristoranti raccomandati ordinando le predizioni in ordine decrescente.
    recommended_restaurants_ids = (-predicted_ratings).argsort()[0][:top_n]

    # Rimozione dei ristoranti già piaciuti dall'utente (valutazione >= 4).
    liked_restaurants_ids = np.where(rating_matrix[user_id] >= 4)[0]
    recommended_restaurants_ids = [r_id for r_id in recommended_restaurants_ids if r_id not in liked_restaurants_ids]
    if not recommended_restaurants_ids:
        print("\n[ℹ️] Nessun nuovo ristorante da consigliare. L'utente ha già valutato positivamente tutti i ristoranti predetti.")
        return

    # Ottengo i dettagli dei ristoranti raccomandati e piaciuti dal dataframe.
    recommended_restaurants = restaurants_df.iloc[recommended_restaurants_ids]
    liked_restaurants = restaurants_df.iloc[liked_restaurants_ids].head(3)

    # Stampo i ristoranti piaciuti.
    print("Dato che ti piacciono:")
    for _, row in liked_restaurants.iterrows():
        print(f"- {row['name']}")

    # Stampo i ristoranti raccomandati.
    print("\nPotrebbero piacerti anche:")
    for idx, (_, row) in enumerate(recommended_restaurants.iterrows(), start=1):
        print(f"{idx}. {row['name']}")