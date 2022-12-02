import socket

SERVER = "127.0.0.1"
PORT = 5000

def client_socket():
    client = socket.socket()  # Création d’un canal de communication permet de creer un socket avec une ip soit un socket tcp
    print(f"Connexion au serveur {SERVER} sur le port {PORT}")
    client.connect((SERVER, PORT))
    #client.setblocking(0)
    print("Je suis connecté")

    data = ""
    while data != "arret" and data != "disconnect":
        message = input("Entrez la donnée à envoyer : ")
        client.send(message.encode())
        print(f"J'ai envoyé un message : {message}")

        data = client.recv(10000).decode()
        print(f"J'ai recu {data}")

    client.close()


if __name__ == '__main__':
    client_socket()