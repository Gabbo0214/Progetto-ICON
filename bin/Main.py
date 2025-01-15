from Lib_install import check_and_install_libraries
check_and_install_libraries()

from Supervised_Learning import supervised_learning
from Neural_Networks import train_autoencoder, get_recommendations
from Knowledge_Graph import create_knowledge_graph, highly_rated_restaurants, most_popular_restaurants, users_who_like_same_category, analyze_knowledge_graph

def display_app_screen():
    """Stampo su schermo un menù per le opzioni."""
    print("\n" + "="*30)
    print("        🍴Glutton         ")
    print("="*30)
    print("1. Lista ristoranti per categoria")
    print("2. Esplora i ristoranti...")
    print("3. Raccomandazioni dell'app")
    print("4. Esci")
    print("="*30)

def display_new_screen():
    """Stampo su schermo un menù per le opzioni."""
    print("\n" + "="*30)
    print("     🍴Glutton Explorer    ")
    print("="*30)
    print("1. Le star del momento")
    print("2. Per i tuoi standard")
    print("3. Utenti con gusti simili")
    print("4. Statistiche del grafo")
    print("5. Esci")
    print("="*30)

def main():
    """Logica centrale del programma."""
    if __name__ == "__main__":
        while True:
            try:
                user_id = int(input("\n[⌨️  ]Inserisci il tuo ID utente (solo il numero): "))
                if user_id >= 0:
                    break
                else:
                    print("\n[❌] ID utente non valido. Inserisci un numero positivo.")
            except ValueError:
                print("\n[❌] ID utente non valido. Inserisci un numero.")
        # Ciclo per menù principale
        app_running = True
        while app_running:
            display_app_screen()
            choice = input("Seleziona un'opzione (1-4): ")
            
            if choice == "1":
                print("\n[📊 ] Esecuzione di Supervised Learning...")
                supervised_learning()
            elif choice == "2":
                print("\n[📊 ] Creazione del grafico...")
                try:
                    graph = create_knowledge_graph('dataset/restaurantList.csv', 'dataset/userRatings.csv')
                    if graph is None:
                        continue
                    # Ciclo per menù explorer
                    explorer_running = True
                    while explorer_running:
                        display_new_screen()
                        new_choice = input("Seleziona un'opzione (1-5): ")
                        if new_choice == "1":
                            most_popular_restaurants(graph)
                        elif new_choice == "2":
                            rating_requested = input("\n[⌨️  ]Inserisci la valutazione minima (1-5): ")
                            highly_rated_restaurants(graph, rating_requested)
                        elif new_choice == "3":
                            users_who_like_same_category(graph, user_id)
                        elif new_choice == "4":
                            analyze_knowledge_graph(graph)
                        elif new_choice == "5":
                            print("\n[↩️ ] Ritorno alla schermata principale.")
                            explorer_running = False
                        else:
                            print("\n[❌] Scelta non valida. Riprova.")
                except Exception as e:
                    print(f"\n[❌] Errore durante la creazione del grafo: {e}")
            elif choice == "3":
                print(f"\n[🔍] Raccomandazioni per l'utente {user_id}...")
                print("\n[🧮] Allenamento Autoencoder in corso...")
                train_autoencoder()
                get_recommendations(user_id)
                print("\n[✔️ ] Raccomandazioni completate.")
            elif choice == "4":
                print("\n[👋] Grazie per aver usato l'app! Arrivederci!")
                app_running = False
            else:
                print("\n[❌] Scelta non valida. Riprova.")

if __name__ == "__main__":
    main()