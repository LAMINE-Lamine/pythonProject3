from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread
import sys

import self as self
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QMainWindow, QComboBox, \
    QDialog, QMessageBox, QTabWidget, QVBoxLayout, QPlainTextEdit, QScrollArea, QTableWidget
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import time
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets


class difserver():
    app = QApplication(sys.argv)
    root = QWidget()

    # create a QTableWidget
    self.__table = QTableWidget(root)
    self.__table.setRowCount(2)
    self.__table.setColumnCount(3)
    self.__table.setGeometry(50, 50, 400, 200)

    # adding header to the table
    headerH = ['ID', 'Name', 'email']
    headerV = ['a', 'b']
    self.__table.setHorizontalHeaderLabels(headerH)
    self.__table.setVerticalHeaderLabels(headerV)


class ScrollLabel(QScrollArea):

    # constructor
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)

        # making widget resizable
        self.setWidgetResizable(True)

        # making qwidget object
        content = QWidget(self)
        self.setWidget(content)

        # vertical box layout
        lay = QVBoxLayout(content)

        # creating label
        self.label = QLabel(content)

        # setting alignment to the text
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # making label multi-line
        self.label.setWordWrap(True)

        # adding label to the layout
        lay.addWidget(self.label)

    # the setText method
    def setText(self, text):
        # setting text to the label
        self.label.setText(text)

    def text(self):
        return self.label.text()


def combobox():
    pass


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ecoute = Thread(target=self.__threadecoute)

        self.socket = socket()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)

        self.__cb = QComboBox()
        self.__port = QLineEdit("")
        self.__ip = QLineEdit("")
        self.__repons = QLineEdit("")
        self.__terminous = ScrollLabel()
        self.__terminous.setStyleSheet("border:1px solid #000")

        self.__port.setPlaceholderText("Done port.")
        self.__ip.setPlaceholderText("done IP")
        self.__repons.setPlaceholderText("ecris ton text")

        self.__ok = QPushButton("Ok")
        self.__envoi = QPushButton("envoi")

        quit = QPushButton("Quitter")
        # Ajouter les composants au grid ayout
        # grid.addWidget(lab,0,1)
        grid.addWidget(self.__port, 1, 2)
        grid.addWidget(self.__ip, 1, 1)
        grid.addWidget(self.__repons, 2, 2)
        grid.addWidget(self.__ok, 1, 0, 1, 1)  # ligne,colonne,hauteur,largueur
        grid.addWidget(self.__envoi, 2, 0, 1, 1)  # ligne,colonne,hauteur,largueur
        grid.addWidget(self.__terminous, 3, 0, 1, 3)

        grid.addWidget(quit)

        quit.clicked.connect(self.__actionQuitter)

        self.__ok.clicked.connect(self.__lancement)
        self.__envoi.clicked.connect(self.__envoimsg)
        self.setWindowTitle("Interface graphique")

    def __actionQuitter(self):
        self.ecoute.join()
        self.socket.close()
        QCoreApplication.exit(0)

    def __lancement(self):
        try:
            HOST = self.__ip.text()
            PORT = int(self.__port.text())
            self.socket.connect((HOST, PORT))
            self.ecoute.start()

            self.__port.setHidden(True)
            self.__ip.setHidden(True)
            self.__ok.setHidden(True)


            # if HOST!= self.__ip.text() and PORT!=int(self.__port.text()):
            # print("erreur de connection port ou ip")



        except:
            self.show_error()


           #except  :

                      #  HOST = self.__ip.text()
            #PORT = int(self.__port.text())
                        #self.socket.connect((HOST, PORT))
                        #self.ecoute.start()

                        #self.__port.setHidden(True)
                        #self.__ip.setHidden(True)
                        #self.__ok.setHidden(True)"""


    def show_error(self):
        errorDialog = QtWidgets.QMessageBox()
        errorDialog.setText('ERROR')
        errorDialog.setWindowTitle('ERROR')
        errorDialog.exec_()

    def __envoimsg(self):

        message = self.__repons.text()
        if message != "":
            self.socket.send(message.encode())
            self.__terminous.setText(self.__terminous.text() + "\nme -> " + message)
            self.__repons.setText("")
        if message == "disconnect" or message == "kill" or message == "reset":
            self.__actionQuitter()

    def __threadecoute(self):
        while True:

            data = self.socket.recv(1024).decode()
            if len(data) == 0:
                break
            self.__terminous.setText(self.__terminous.text() + "\n" + data)
            if data == "disconnect" or data == "kill" or data == "reset":
                break


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 500)
    window.show()
    app.exec()
