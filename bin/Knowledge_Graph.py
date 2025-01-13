import networkx as nx
import pandas as pd

def create_knowledge_graph(restaurant_file, ratings_file):
    """
    Crea un grafo di conoscenza a partire dai file CSV di ristoranti e recensioni.
    """
    try:
        restaurants = pd.read_csv(restaurant_file)
        ratings = pd.read_csv(ratings_file)
    except FileNotFoundError:
        print(f"\n[❌] Errore: Uno o entrambi i file non trovati: {restaurant_file}, {ratings_file}")
        return None

    G = nx.Graph()

    for _, restaurant in restaurants.iterrows():
        restaurant_node = f"restaurant_{restaurant['id']}"
        G.add_node(restaurant_node, label="restaurant", name=restaurant['name'])
        categories = restaurant['categories'].split(',')
        for category in categories:
            category = category.strip()
            category_node = f"category_{category}"
            G.add_node(category_node, label="category", name=category)
            G.add_edge(restaurant_node, category_node, relation="is_a")

    for _, rating in ratings.iterrows():
        user_node = f"user_{rating['user_id']}"
        restaurant_node = f"restaurant_{rating['restaurant_id']}"
        if not G.has_node(user_node):
            G.add_node(user_node, label="user", user_id=rating['user_id'])
        G.add_edge(user_node, restaurant_node, weight=rating['rating'], relation="rated")

    print("\n[✔️] Grafo creato con successo.")
    return G

def highly_rated_restaurants(G, min_rating):
    """
    Restituisce i ristoranti con una valutazione media superiore o uguale a min_rating.
    """
    if G is None:
        return
    try:
        min_rating = float(min_rating)
    except ValueError:
        print("\n[❌] Valutazione non valida. Inserisci un numero.")
        return

    print(f"\n[️] Ristoranti con valutazione media >= {min_rating}:")
    restaurant_ratings = {}

    for u, v, data in G.edges(data=True):
        if data.get('relation') == 'rated': #Controllo che sia un edge di rating
            restaurant = v if v.startswith("restaurant_") else u
            if restaurant not in restaurant_ratings:
                restaurant_ratings[restaurant] = []
            restaurant_ratings[restaurant].append(data['weight'])

    for restaurant, ratings in restaurant_ratings.items():
        if ratings:
            avg_rating = sum(ratings) / len(ratings)
            if avg_rating >= min_rating:
                print(f"- {G.nodes[restaurant]['name']} (Media: {avg_rating:.2f})")

def most_popular_restaurants(G):
    """
    Restituisce i 10 ristoranti più popolari (con più recensioni).
    """
    if G is None:
        return
    print("\n[] Ristoranti più popolari:")
    restaurant_popularity = {}

    for node, data in G.nodes(data=True):
        if data.get('label') == 'restaurant':
            restaurant_popularity[node] = len([n for n in G.neighbors(node) if n.startswith("user_")])

    sorted_restaurants = sorted(restaurant_popularity.items(), key=lambda x: x[1], reverse=True)

    for restaurant, connections in sorted_restaurants[:10]:
        print(f"- {G.nodes[restaurant]['name']} (Recensioni: {connections})")

def users_who_like_same_category(G, user_id, max_users=15):
    """
    Trova utenti con gusti simili (stesse categorie di ristoranti preferite).
    """
    if G is None:
        return
    user_node = f"user_{user_id}"
    if not G.has_node(user_node):
        print(f"L'utente {user_id} non è presente nel grafo.")
        return

    liked_categories = set()
    for restaurant in G.neighbors(user_node):
        if restaurant.startswith("restaurant_") and G[user_node][restaurant].get('relation') == 'rated' and G[user_node][restaurant].get('weight', 0) >= 3:
            liked_categories.update(n for n in G.neighbors(restaurant) if n.startswith("category_"))

    similar_users = {}
    for category in liked_categories:
        for restaurant in G.neighbors(category):
            if restaurant.startswith("restaurant_"):
                for other_user in G.neighbors(restaurant):
                    if other_user.startswith("user_") and other_user != user_node:
                        if other_user not in similar_users:
                            similar_users[other_user] = {'high_ratings': 0, 'common_categories': set()}
                        if G.has_edge(user_node, restaurant) and G.has_edge(other_user, restaurant) and G[user_node][restaurant].get('relation') == 'rated' and G[user_node][restaurant].get('weight', 0) >= 3 and G[other_user][restaurant].get('weight', 0) >= 3:
                            similar_users[other_user]['high_ratings'] += 1
                            similar_users[other_user]['common_categories'].add(G.nodes[category]['name'])

    sorted_users = sorted(similar_users.items(), key=lambda x: x[1]['high_ratings'], reverse=True)

    print(f"\n[] Utenti con gusti simili a te:")
    found = False
    for user, similarity in sorted_users[:max_users]:
        if similarity['high_ratings'] > 0:
            print(f"- {user} (Ristoranti simili che vi piacciono: {similarity['high_ratings']}, Categorie in comune: {', '.join(similarity['common_categories'])})")
            found = True

    if not found:
        print("[] Nessun utente trovato con gusti simili.")

def analyze_knowledge_graph(G):
    """
    Analizza il grafo di conoscenza e stampa statistiche su di esso.
    """
    if G is None:
        return

    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    num_restaurants = len([node for node, data in G.nodes(data=True) if data.get('label') == 'restaurant'])
    num_categories = len([node for node, data in G.nodes(data=True) if data.get('label') == 'category'])
    num_users = len([node for node, data in G.nodes(data=True) if data.get('label') == 'user'])
    density = nx.density(G)

    print("\n[] Analisi del Grafo di Conoscenza:")
    print(f"- Numero totale di nodi: {num_nodes}")
    print(f"- Numero di ristoranti: {num_restaurants}")
    print(f"- Numero di categorie: {num_categories}")
    print(f"- Numero di utenti: {num_users}")
    print(f"- Numero totale di archi: {num_edges}")
    print(f"- Densità del grafo: {density:.4f}")