import socket
import os
import sys , subprocess

host = "127.0.0.1"
port = 5000


def execute_cmd(cmd):
#    ret = str(subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT))
#    return ret
    return f"J'ai exécuté {cmd}"

def hostname():
    cmd=socket.gethostname()
    return cmd

def ipconfig():
    host=socket.gethostname()
    cmd = socket.gethostbyname(host)
    #cmd = subprocess.Popen("ipconfig",encoding='cp850',shell=True)
    return cmd


def ram():
    cmd = subprocess.check_output("wmic computersystem get totalphysicalmemory.", shell=True).decode()
    return cmd

def Os():
    cmd=sys.platform
    if cmd == "win32":
        cmd = subprocess.check_output("ver", shell=True).decode()
        return cmd
    else:
        return cmd

def cpu ():
    cmd = subprocess.check_output("wmic cpu get caption, deviceid, name, numberofcores, maxclockspeed, status", shell=True).decode()
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

                if data == 'ip':
                    res = ipconfig()
                    conn.send(res.encode())
                    print(f'CA BIEN ETAIT FAIT IPPPPPP {res}')

                elif data == 'sh cpu':
                    res = cpu()
                    conn.send(res.encode())
                    print(f'voici le cpu de la machine: {res}')

                elif data == 'sh ram':
                    res = ram()
                    conn.send(res.encode())
                    print(f'voici la ram de la machine: {res}')

                elif data == 'os':
                    res = Os()
                    conn.send(res.encode())
                    print(f"on a l'OS {res}")

                elif data == "bye" or data == "arret":
                    print ("fermeture du server ")
                    conn.send("arret".encode())
                    break

                elif data == "disconnect":
                    print ("deconnection du client au server")
                    conn.send("disconnect".encode())
                    break

                #fonction kill
                elif data == "kill":
                    conn.send("disconnect".encode())
                    conn.close()
                    server.close()
                    sys.exit(0)

                elif data == "reset":
                    conn.send("reset".encode())
                    conn.close()
                    server.close()
                    print("relance du server")
                    server = socket.socket()  # Création d’un canal de communication permet de creer un socket avec une ip soit un socket tcp
                    server.bind((host, port))
                    server.listen(1)
                    print("En attente d'un client")
                    break

                elif data == "hello":
                    message = "hello"
                    conn.send(message.encode())  # SEND
                    print(f"J'ai envoyé un message {message}")

                else:
                    # DOS:dir ou linux:dir
                    # dir
                    message = execute_cmd(data)
                    conn.send(message.encode())  # SEND
                    print(f"J'ai envoyé un message {message}")

            conn.close() # fermeture avec le client

        server.close()


if __name__ == '__main__':
    server_socket()
