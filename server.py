import socket
import os
import sys , subprocess
import psutil



host = "127.0.0.1"
port = int(input("port:"))

########


def Hostname():
    cmd=socket.gethostname()
    return cmd

def ipconfig():
    host=socket.gethostname()
    cmd = socket.gethostbyname(host)
    #cmd = subprocess.Popen("ipconfig",encoding='cp850',shell=True)
    return cmd


def ram():
    cmd= str(f"-La memoire total:{psutil.virtual_memory()[0]} octet\n-la memoire utiliser:{psutil.virtual_memory()[1]} octet\n-la memoire disponible:{psutil.virtual_memory()[4]} octet")
    return cmd

def Os():
    cmd=sys.platform
    if cmd == "win32":
        cmd = subprocess.check_output("ver", shell=True).decode()
        return cmd
    else:
        return cmd

import client
def Ping (data):
    cmd = subprocess.getoutput(data)
    return cmd


def versionn():
    cmd=str(subprocess.check_output("python --version", shell=True))
    return cmd


def cpu ():
    cmd = str(f"CPU utiliser :{psutil.cpu_percent()}%")

    return cmd






#os=retourner systeme dexploitation cpu=envoi pourcentage utilisation cpu ram=renvoi les ram du pc  retour versionde python  faire logs

def server_socket():
    while True:
        server = socket.socket()  #Création d’un canal de communication permet de creer un socket avec une ip soit un socket tcp
        server.bind((host, port))
        server.listen(1)

        while True:
            print("En attente d'un client")
            conn, address = server.accept()  #ACCEPT
            print(f"Un client s'est connecté à partir de {address}")

            data = ""
            while data != "bye" or data != "arret":

                data = conn.recv(1024).decode()#RECEIV
                print(f"Data = {data}")









                if data.lower() == 'ip':
                    res = ipconfig()
                    conn.send(res.encode())
                    print(f'CA BIEN ETAIT FAIT IPPPPPP {res}')

                elif data.lower()=='hostname':
                    res=Hostname()
                    conn.send(res.encode())
                    print(f'voici lhostname:{res}')


                elif data.lower()[0:4] == "ping":
                    res = Ping(data)
                    conn.send(res.encode())
                    print(f'voici le ping: {res}')


                elif data[0:4] =="DOS:":
                    re = data.split(':')[1]
                    res = subprocess.check_output(re, shell=True).decode("cp850")
                    conn.send(res.encode())
                    print(f"voici{res}")


                elif data[0:4] =="LINUX:":
                    re = data.split(':')[1]
                    res = subprocess.check_output(re, shell=True).decode("cp850")
                    conn.send(res.encode())
                    print(f"voici{res}")


                elif data.lower()== 'cpu':
                    res = cpu()
                    conn.send(res.encode())
                    print(f'voici le cpu de la machine: {res}')

                elif data.lower()== 'ram':
                    res = ram()
                    conn.send(res.encode())
                    print(f'voici la ram de la machine: {res}')

                elif data.lower()== 'os':
                    res = Os()
                    conn.send(res.encode())
                    print(f"on a l'OS {res}")

                elif data.lower() == 'Ping':
                    res = ping("")
                    conn.send(res.encode())
                    print(f"on fais le ping: {res}")

                elif data.lower() == 'python --version':
                    res = versionn()
                    conn.send(res.encode())
                    print(f"la version: {res}")

                elif data.lower()== "bye" or data.lower()== "arret":
                    print ("fermeture du server ")
                    conn.send("arret".encode())
                    break

                elif data.lower()== "disconnect":
                    print ("deconnection du client au server")
                    conn.send("disconnect".encode())
                    break

                #fonction kill
                elif data.lower()== "kill":
                    conn.send("disconnect".encode())
                    conn.close()
                    server.close()
                    sys.exit(0)

                elif data.lower()== "reset":
                    conn.send("reset".encode())
                    conn.close()
                    server.close()
                    print("relance du server")
                    server = socket.socket()  # Création d’un canal de communication permet de creer un socket avec une ip soit un socket tcp
                    server.bind((host, port))
                    server.listen(1)
                    print("En attente d'un client")
                    break

                elif data.lower()== "hello":
                    message = "hello"
                    conn.send(message.encode())  # SEND
                    print(f"J'ai envoyé un message {message}")

                else:
                    # DOS:dir ou linux:dir
                    message="command invalide"
                    conn.send(message.encode())

                    print(f"J'ai envoyé un message {message}")





            conn.close() # fermeture avec le client

        server.close()


if __name__ == '__main__':
    server_socket()
