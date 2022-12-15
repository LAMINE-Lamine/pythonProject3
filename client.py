from socket import socket
from threading import Thread
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QMainWindow, QComboBox, \
    QTabWidget, QVBoxLayout, QScrollArea, QMessageBox
from PyQt5.QtCore import QCoreApplication, Qt


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

        self.verticalScrollBar().rangeChanged.connect(self.scroll)

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

    def scroll(self):
        scrollbar = self.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())


def combobox():
    pass


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

        self.__port.setPlaceholderText("Done port.")
        self.__ip.setPlaceholderText("done IP")

        self.__ok = QPushButton("Ok")
        self.__envoi = QPushButton("envoi")

        # Ajouter les composants au grid ayout
        # grid.addWidget(lab,0,1)
        self.__stop = False
        self.__tabwidget = QTabWidget()
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

