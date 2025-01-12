from Lib_install import check_and_install_libraries
check_and_install_libraries()
    
from Supervised_Learning import supervised_learning
from Neural_Networks import train_autoencoder, get_recommendations
from Knowledge_Graph import create_knowledge_graph, highly_rated_restaurants, most_popular_restaurants, users_who_like_same_category

def display_app_screen():

    print("\n" + "="*30)
    print("        🍴 Glutton         ")
    print("="*30)
    print("1. Lista ristoranti per categoria")
    print("2. Esplora i ristoranti...")
    print("3. Raccomandazioni dell'app")
    print("4. Esci")
    print("="*30)

def display_new_screen():

    print("\n" + "="*30)
    print("    🍴 Glutton Explorer     ")
    print("="*30)
    print("1. Le star del momento")
    print("2. Per i tuoi standard")
    print("3. Utenti con gusti simili")
    print("4. Esci")
    print("="*30)
    
def main():
    
    user_id = input("\n[⌨️  ]Inserisci il tuo ID utente (solo il numero): ")
            
    while True:
        display_app_screen()
        choice = input("Seleziona un'opzione (1-4): ")
        
        if choice == "1":
            print("\n[📊] Esecuzione di Supervised Learning...")
            supervised_learning()
        elif choice == "2":
            print("\n[🔍] Creazione del grafico...")
            graph = create_knowledge_graph('dataset/restaurantList.csv', 'dataset/userRatings.csv')
            
            while True:
                display_new_screen()
                new_choice = input("Seleziona un'opzione (1-4): ")
                if new_choice == "1":
                    most_popular_restaurants(graph)
                elif new_choice == "2":
                    rating_requested = input("\n[⌨️  ]Inserisci la valutazione minima (1-5): ")
                    highly_rated_restaurants(graph, rating_requested)
                elif new_choice == "3":
                    users_who_like_same_category(graph, user_id)
                elif new_choice == "4":
                    print("\n[👋] Ritorno alla schermata principale.")
                    break
                else:
                    print("\n[❌] Scelta non valida. Riprova.")
            
        elif choice == "3":
            print(f"\n[🎯] Raccomandazioni per l'utente {user_id}...")
            print("\n[🤖] Allenamento Autoencoder in corso...")
            train_autoencoder()
            print("\n[✔️ ] Autoencoder allenato con successo.")
            get_recommendations(int(user_id))
            print("\n[✔️ ] Raccomandazioni completate.")
        elif choice == "4":
            print("\n[👋] Grazie per aver usato l'app! Arrivederci!")
            break
        else:
            print("\n[❌] Scelta non valida. Riprova.")

#Eseguo il main
if __name__ == "__main__":
    main()