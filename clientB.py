from threading import Thread
import socket

Host = "127.0.0.1"
Port = 5000

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((Host,Port))

def Send(client):
    while True:
        client.send(input("Ecrit ton message :").encode('utf8'))

def Reception(client):
    while True:
        req = client.recv(10000).decode('utf8')
        print("Serveur a envoyer :",req)






if __name__ == '__main__':
    client_socket()
envoi = Thread(target=Send,args=[client])
recep = Thread(target=Reception,args=[client])
envoi.start()
recep.start()

envoi.join()
recep.join()