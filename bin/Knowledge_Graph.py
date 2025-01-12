import networkx as nx
import pandas as pd

def create_knowledge_graph(restaurant_file, ratings_file):
    
    #Carico i dati dai file CSV
    restaurants = pd.read_csv(restaurant_file)
    ratings = pd.read_csv(ratings_file)

    #Creo il grafo
    G = nx.Graph()

    #Aggiungo nodi per i ristoranti e categorie
    for _, restaurant in restaurants.iterrows():
        G.add_node(f"restaurant_{restaurant['id']}", label="restaurant", name=restaurant['name'])
        G.add_node(f"category_{restaurant['categories']}", label="category")
        G.add_edge(f"restaurant_{restaurant['id']}", f"category_{restaurant['categories']}")

    #Aggiungo nodi per gli utenti e per le recensioni
    for _, rating in ratings.iterrows():
        user_node = f"user_{rating['user_id']}"
        restaurant_node = f"restaurant_{rating['restaurant_id']}"

        #Aggiungi il nodo dell'utente se non esiste già
        if not G.has_node(user_node):
            G.add_node(user_node, label="user", user_id=rating['user_id'])
        
        #Crea l'arco con il peso della recensione
        G.add_edge(user_node, restaurant_node, weight=rating['rating'])
    
    print("\n[✔️ ] Grafo creato con successo.")
    return G

#Visualizza i ristoranti con recensioni migliori
def highly_rated_restaurants(G, min_rating):
    min_rating = float(min_rating)
    print(f"\n[🍽️ ] Ristoranti con valutazione media >= {min_rating}:")
    restaurant_ratings = {}
    
    for edge in G.edges(data=True):
        if 'weight' in edge[2]:
            restaurant = edge[1] if edge[0].startswith("user_") else edge[0]
            if restaurant not in restaurant_ratings:
                restaurant_ratings[restaurant] = []
            restaurant_ratings[restaurant].append(edge[2]['weight'])
    
    for restaurant, ratings in restaurant_ratings.items():
        avg_rating = sum(ratings) / len(ratings)
        if avg_rating >= min_rating:
            print(f"- {G.nodes[restaurant]['name']} (Media: {avg_rating:.2f})")

#Funzione per trovare i ristoranti più popolari
def most_popular_restaurants(G):
    print("\n[🌟] Ristoranti più popolari:")
    restaurant_popularity = {}

    #Conta il numero di connessioni per ogni ristorante
    for node, data in G.nodes(data=True):
        if data['label'] == 'restaurant':
            restaurant_popularity[node] = len(list(G.neighbors(node)))
    
    #Ordina i ristoranti per popolarità (numero di connessioni)
    sorted_restaurants = sorted(restaurant_popularity.items(), key=lambda x: x[1], reverse=True)
    
    for restaurant, connections in sorted_restaurants[:10]:  #Mostra i primi 10
        print(f"- {G.nodes[restaurant]['name']} (Recensioni: {connections})")

def users_who_like_same_category(G, user_id, max_users=15):
    user_node = f"user_{user_id}"
    if not G.has_node(user_node):
        print(f"L'utente {user_id} non è presente nel grafo.")
        return
    
    #Trova i ristoranti recensiti dall'utente
    reviewed_restaurants = [neighbor for neighbor in G.neighbors(user_node) if neighbor.startswith("restaurant_")]
    
    #Trova le categorie associate ai ristoranti recensiti con voto alto
    liked_categories = set()
    for restaurant in reviewed_restaurants:
        if G.has_edge(user_node, restaurant):  #Verifica se esiste l'arco
            user_rating = G[user_node][restaurant].get('weight', 0)
            if user_rating >= 3:
                for neighbor in G.neighbors(restaurant):
                    if neighbor.startswith("category_"):
                        liked_categories.add(neighbor)
    
    #Trova utenti che hanno recensito ristoranti nelle stesse categorie
    similar_users = {}
    for category in liked_categories:
        for restaurant in G.neighbors(category):
            if restaurant.startswith("restaurant_"):
                for other_user in G.neighbors(restaurant):
                    if other_user.startswith("user_") and other_user != user_node:
                        if other_user not in similar_users:
                            similar_users[other_user] = {'high_ratings': 0}
                        
                        #Verifico le valutazioni alte nella stessa categoria
                        if G.has_edge(user_node, restaurant) and G.has_edge(other_user, restaurant):
                            user_rating = G[user_node][restaurant].get('weight', 0)
                            other_user_rating = G[other_user][restaurant].get('weight', 0)
                            if user_rating >= 3 and other_user_rating >= 3:
                                similar_users[other_user]['high_ratings'] += 1
    
    #Ordina gli utenti per il numero di ristoranti con valutazioni alte
    sorted_users = sorted(
        similar_users.items(),
        key=lambda x: x[1]['high_ratings'],
        reverse=True
    )
    
    #Stampo i primi 15 utenti che hanno almeno un ristorante simile con valutazione alta
    print(f"\n[👥] Utenti con gusti simili a te:")
    found = False  #Flag per verificare se ci sono utenti con ristoranti simili
    for user, similarity in sorted_users[:max_users]:
        if similarity['high_ratings'] > 0:
            print(f"- {user} (Ristoranti simili che vi piacciono: {similarity['high_ratings']})")
            found = True
    
    if not found:
        print("[😟]Nessun utente trovato con gusti simili.")