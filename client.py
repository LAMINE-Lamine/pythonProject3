from socket import socket
from threading import Thread
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QMainWindow, QComboBox, \
    QTabWidget, QVBoxLayout, QScrollArea, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5 import QtCore


class ScrollLabel(QScrollArea):
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)
        self.setWidgetResizable(True)
        content = QWidget(self)
        self.setWidget(content)
        lay = QVBoxLayout(content)
        self.label = QLabel(content)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.verticalScrollBar().rangeChanged.connect(self.scroll)
        self.label.setWordWrap(True)
        lay.addWidget(self.label)

    def setText(self, text):
        self.label.setText(text)

    def text(self):
        return self.label.text()

    def scroll(self):
        scrollbar = self.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())


def combobox():
    pass


class baseDeDonnee(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.__parent = parent
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.__table_csv = QTableWidget()
        self.__ip_edit = QLineEdit()
        self.__port_edit = QLineEdit()
        self.__confirm = QPushButton('OK')
        self.__confirm.clicked.connect(self.__ajouter_ligne)
        self.grid.addWidget(self.__table_csv,0,0,1,3)
        self.grid.addWidget(self.__ip_edit,1,0)
        self.grid.addWidget(self.__port_edit,1,1)
        self.grid.addWidget(self.__confirm,1,2)
        self.__table_csv.setRowCount(0)
        self.__table_csv.setColumnCount(1)
        try:
            with open('csv_doc.csv','r') as file:
                lines = file.readlines()
                for line in lines:
                    line = line.replace('\n','')
                    elements = line.split(':')
                    if len(elements) == 2:
                        if elements[1].isdigit() and len(elements[0]) > 0:
                            lignes = self.__table_csv.rowCount()
                            self.__table_csv.setRowCount(lignes + 1)
                            self.__table_csv.setItem(lignes,0,QTableWidgetItem(line))
        except:
            with open('csv_doc.csv','w') as file:
                file.write('')
        self.__table_csv.horizontalHeader().setStretchLastSection(True)
        self.__table_csv.verticalHeader().setVisible(False)
        self.__table_csv.setHorizontalHeaderLabels(['Serveurs'])
        self.__table_csv.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.__table_csv.setFocusPolicy(QtCore.Qt.NoFocus)
        self.__table_csv.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.__table_csv.resizeRowsToContents()
        self.__table_csv.doubleClicked.connect(self.__connecter_serveur)
    
    def __ajouter_ligne(self):
        ip = self.__ip_edit.text()
        port = self.__port_edit.text()
        if port.isdigit() and len(ip) > 0:
            ligne = ip + ':' + port
            try:
                with open('csv_doc.csv','a') as file:
                    file.write('\n' + ligne)
            except:
                with open('csv_doc.csv','w') as file:
                    file.write(ligne)
            lignes = self.__table_csv.rowCount()
            self.__table_csv.setRowCount(lignes + 1)
            self.__table_csv.setItem(lignes,0,QTableWidgetItem(ligne))
            self.__ip_edit.setText('')
            self.__port_edit.setText('')
            self.__table_csv.resizeRowsToContents()
    
    def __connecter_serveur(self):
        ligne = self.__table_csv.currentRow()
        ligne = self.__table_csv.item(ligne, 0).text().split(':')
        if len(ligne) == 2:
            if ligne[1].isdigit():
                ip = ligne[0]
                port = ligne[1]
                self.__parent.lancement_fichier_csv(ip, port)

class connection(QWidget):
    def __init__(self, connection, parent):
        super().__init__()
        self.__layout = QGridLayout()
        self.setLayout(self.__layout)
        self.__connection = connection
        self.__parent = parent
        self.__stop = False
        self.__terminous = ScrollLabel()
        self.__terminous.setStyleSheet("margin:0;padding:0")
        self.__commandinput = QLineEdit()
        self.__commandinput.setPlaceholderText('INSERER COMMANDE')
        self.__commandinput.returnPressed.connect(self.__send_message)
        self.__layout.addWidget(self.__terminous, 0, 0)
        self.__layout.addWidget(self.__commandinput, 1, 0)
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__layout.setSpacing(0)
        self.__threadecoute = Thread(target=self.__ecoute)
        self.__threadecoute.start()

    def __ecoute(self):
        while not self.__parent.stopped() and not self.__stop:
            try:
                data = self.__connection.recv(1024).decode()
                if data == 'disconnect' or data == 'reset':
                    self.__close()
                else:
                    self.__terminous.setText(self.__terminous.text() + '\n' + data)
            except:
                pass

    def __send_message(self):
        command = self.__commandinput.text()
        self.__commandinput.setText('')
        self.__terminous.setText(self.__terminous.text() + '\nMoi > ' + command)
        try:
            self.__connection.send(command.encode())
        except:
            pass

    def __close(self):
        self.__stop = True
        self.deleteLater()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.__socket = socket()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)
        self.__cb = QComboBox()
        self.__port = QLineEdit("6000")
        self.__ip = QLineEdit("127.0.0.1")

        self.__port.setPlaceholderText("Inserer PORT")
        self.__ip.setPlaceholderText("Inserer IP")

        self.__ok = QPushButton("Ok")
        self.__envoi = QPushButton("envoi")
        
        self.__csv = baseDeDonnee(self)

        # Ajouter les composants au grid ayout
        # grid.addWidget(lab,0,1)
        self.__stop = False
        self.__tabwidget = QTabWidget()
        self.__tabwidget.addTab(self.__csv, 'CSV')
        grid.addWidget(self.__port, 1, 2)
        grid.addWidget(self.__ip, 1, 1)
        grid.addWidget(self.__ok, 1, 0)  # ligne,colonne,hauteur,largueur
        grid.addWidget(self.__tabwidget, 2, 0, 1, 3)
        self.__ok.clicked.connect(self.__lancement)
        self.setWindowTitle("Interface graphique")

    def __actionQuitter(self):
        self.__stop = True
        self.__socket.close()
        QCoreApplication.exit(0)

    def stopped(self) -> bool:
        return self.__stop

    def closeEvent(self, event):
        self.__actionQuitter()
        event.accept()

    def __lancement(self):
        client_socket = socket()
        HOST = self.__ip.text()
        PORT = self.__port.text()
        if PORT.isdigit():
            PORT = int(PORT)
            try:
                client_socket.connect((HOST, PORT))
                client_socket.setblocking(False)
                tab = connection(client_socket, self)
                self.__tabwidget.addTab(tab, str(HOST) + ':' + str(PORT))
            except:
                self.show_error(f'Erreur lors de la connection vers {HOST}:{PORT}')
        else:
            self.show_error('Veuillez insérer un numéro pour le port!')
    
    def lancement_fichier_csv(self, HOST: str, PORT: int):
        client_socket = socket()
        if PORT.isdigit():
            PORT = int(PORT)
            try:
                client_socket.connect((HOST, PORT))
                client_socket.setblocking(False)
                tab = connection(client_socket, self)
                self.__tabwidget.addTab(tab, str(HOST) + ':' + str(PORT))
            except:
                self.show_error(f'Erreur lors de la connection vers {HOST}:{PORT}')
        else:
            self.show_error('Veuillez insérer un numéro pour le port!')

    def show_error(self, err=None):
        errorDialog = QMessageBox()
        if err is not None:
            errorDialog.setText(str(err))
        else:
            errorDialog.setText("Une erreur s'est produite")
        errorDialog.setWindowTitle('ERROR')
        errorDialog.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 500)
    window.show()
    app.exec()
