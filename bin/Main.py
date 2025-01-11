from Lib_install import check_and_install_libraries
check_and_install_libraries()
    
from Supervised_Learning import supervised_learning
from Neural_Networks import train_autoencoder, get_recommendations

def main():
    #Richiamo una a una le funzioni importanti
    supervised_learning()
    train_autoencoder()
    user_id = 1
    get_recommendations(user_id)
    
#Eseguo il main
if __name__ == "__main__":
    main()