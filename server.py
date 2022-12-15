import socket
import os
import sys, subprocess
import psutil

host = "127.0.0.1"
# port = int(input("port:"))
port = 8000


def Hostname():
    cmd = socket.gethostname()
    return cmd


def ipconfig():
    host = socket.gethostname()
    cmd = socket.gethostbyname(host)
    return cmd


def ram():
    cmd = str(
        f"-La memoire total:{psutil.virtual_memory()[0]} octet\n-la memoire utiliser:{psutil.virtual_memory()[1]} octet\n-la memoire disponible:{psutil.virtual_memory()[4]} octet")
    return cmd


def Os():
    cmd = sys.platform
    if cmd == "win32":
        cmd = subprocess.check_output("ver", shell=True).decode()
        return cmd
    else:
        return cmd


def ping(data):
    if sys.platform == 'win32':
        cmd = subprocess.getoutput(data)
    elif sys.platform == 'linux' or sys.platform == 'linux2':
        cmd = subprocess.getoutput('ping -c 4 ' + data.split(' ')[1])
    else:
        cmd = "Le system d'exploitation de la machine n'est pas reconnue par le serveur et il ne peut donc pas effectuer cette commande"
    return cmd


def version():
    cmd = str(subprocess.check_output("python --version", shell=True))
    return cmd


def cpu():
    cmd = str(f"CPU utiliser :{psutil.cpu_percent()}%")

    return cmd


# os=retourner systeme dexploitation cpu=envoi pourcentage utilisation cpu ram=renvoi les ram du pc  retour versionde python  faire logs

def server_socket():
    while True:
        server = socket.socket()  # Création d’un canal de communication permet de creer un socket avec une ip soit un socket tcp
        server.bind((host, port))
        server.listen(1)
        while True:
            print("En attente d'un client")
            conn, address = server.accept()  # ACCEPT
            print(f"Un client s'est connecté à partir de {address}")
            data = ""
            while data != "bye" or data != "arret":
                try:
                    data = conn.recv(1024).decode()  # RECEIV
                    if data is not None:
                        if data.lower() == 'ip':
                            res = ipconfig()
                            conn.send(res.encode())

                        elif data.lower() == 'name':
                            res = Hostname()
                            conn.send(res.encode())

                        elif data.lower()[0:4] == "ping":
                            res = ping(data)
                            conn.send(res.encode())

                        elif data[0:4].lower() == "dos:":#7 envrion
                            if sys.platform == 'win32':#
                                re = data.split(':', 1)[1]
                                p = subprocess.Popen(re, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                                output = p.stdout.read()
                                if len(output) == 0:
                                    output = p.stderr.read()
                                try:
                                    output = output.decode('utf-8')
                                except:
                                    output = output.decode('cp850')
                                conn.send(output.encode())
                            else:
                                conn.send('Cette machine n\'est pas une machine windows. Il est impossible d\'éffectuer cette commande'.encode())


                        elif data[0:11].lower() == "powershell:":
                            if sys.platform == 'win32':#
                                re = data.split(':', 1)[1]
                                p = subprocess.Popen(f"""re -command "{re}" """, stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding='cp850', shell=True)#command systeme
                                output = p.stdout.read()
                                if len(output) == 0:
                                    output = p.stderr.read()
                                try:
                                    output = output.decode('utf-8')
                                except:
                                    output = output.decode('cp850')
                                conn.send(output.encode())
                            else:
                                conn.send('Cette machine n\'est pas une machine windows. Il est impossible d\'éffectuer cette commande'.encode())




                        elif data[0:4].lower() == "linux:":
                            if sys.platform == 'linux' or sys.platform == 'linux2':
                                re = data.split(':', 1)[1]
                                p = subprocess.Popen(re, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', shell=True)
                                output = p.stdout.read()
                                if len(output) == 0:
                                    output = p.stderr.read()
                                conn.send(output.encode())
                            else:
                                conn.send('Cette machine n\'est pas une machine Linux. Il est impossible d\'éffectuer cette commande'.encode())

                        elif data.lower() == 'cpu':
                            res = cpu()
                            conn.send(res.encode())

                        elif data.lower() == 'ram':
                            res = ram()
                            conn.send(res.encode())

                        elif data.lower() == 'os':
                            res = Os()
                            conn.send(res.encode())

                        elif data.lower() == 'python --version':
                            res = version()
                            conn.send(res.encode())

                        elif data.lower() == "bye" or data.lower() == "arret":
                            print("fermeture du server ")
                            conn.send("arret".encode())
                            break

                        elif data.lower() == "disconnect":
                            print("deconnection du client au server")
                            conn.send("disconnect".encode())
                            break

                        #fonction kill
                        elif data.lower() == "kill":
                            conn.send("disconnect".encode())
                            conn.close()
                            server.close()
                            sys.exit(0)


                        elif data.lower() == "reset":
                            # server = socket.socket()
                            # server.bind((host,port))
                            # server.listen(1)
                            # print(f"{host}-{port}")
                            conn.send("reset".encode())
                            conn.close()
                            server.close()

                            server = socket.socket()  #Création d’un canal de communication permet de creer un socket avec une ip soit un socket tcp
                            server.bind((host, port))
                            server.listen(1)
                            print("En attente d'un client")
                            break

                        elif data.lower() == "hello":
                            message = "hello"
                            conn.send(message.encode())  # SEND
                            print(f"J'ai envoyé un message {message}")

                        else:
                            # DOS:dir ou linux:dir
                            message = "command invalide"
                            conn.send(message.encode())

                            print(f"J'ai envoyé un message {message}")
                except:
                    conn.close()
                    break

            conn.close()  # fermeture avec le client


if __name__ == '__main__':
    server_socket()
