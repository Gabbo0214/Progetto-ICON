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

        G.add_node(user_node, label="user")
        if G.has_node(restaurant_node):
            G.add_edge(user_node, restaurant_node, weight=rating['rating'])

    #Visualizzo le informazioni sul grafo
    print("Numero di nodi:", G.number_of_nodes())
    print("Numero di archi:", G.number_of_edges())
    
    return G