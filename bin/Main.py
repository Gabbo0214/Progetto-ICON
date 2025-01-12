from Lib_install import check_and_install_libraries
check_and_install_libraries()
    
from Supervised_Learning import supervised_learning
from Neural_Networks import train_autoencoder, get_recommendations
from Knowledge_Graph import create_knowledge_graph

def display_phone_screen():
    """
    Simulo lo schermo di un telefono per l'interazione con l'utente.
    """
    print("\n" + "="*30)
    print("        🍴 Glutton         ")
    print("="*30)
    print("1. Lista ristoranti per categoria")
    print("2. Grafico ristoranti consigliati")
    print("3. Ottieni Raccomandazioni")
    print("4. Esci")
    print("="*30)

def main():
    
    while True:
        display_phone_screen()
        choice = input("Seleziona un'opzione (1-4): ")
        
        if choice == "1":
            print("\n[📊] Esecuzione di Supervised Learning...")
            supervised_learning()
        elif choice == "2":
            print("\n[🔍] Creazione del grafico...")
            graph = create_knowledge_graph('dataset/restaurantList.csv', 'dataset/userRatings.csv')
            print("\n[✔️ ] Grafico creato con successo.")
        elif choice == "3":
            user_id = input("\nInserisci l'ID utente per le raccomandazioni: ")
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