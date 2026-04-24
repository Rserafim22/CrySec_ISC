import sys
import threading
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtUiTools import QUiLoader
import connection_manager, message_manager, utils, ui

ADDRESS = 'vlbelintrocrypto.hevs.ch'
PORT = 6000

class App(QWidget):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        self.ui = loader.load("Secure_chat.ui")
        main_layout = QVBoxLayout(self) 
        main_layout.addWidget(self.ui)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.client = connection_manager.Client()
        self.client.connect(ADDRESS, PORT)
        self.messager = message_manager.MessageHandler(self.client)
        
        self.bridge = ui.UIBridge(self.ui, self.client, self.messager)
        
        if self.client.connection_state:
            self.thread_ecoute = threading.Thread(target=self.gui_listen_loop, daemon=True)
            self.thread_ecoute.start()
            self.bridge.new_message_signal.emit("Serveur", "Connecté au serveur avec succès !")
        else:
            self.bridge.new_message_signal.emit("Error", "Échec de la connexion au serveur.")

    def gui_listen_loop(self):
        while self.client.connection_state:
            data = self.client.receive()
            if data:
                self.messager.add_data(data)
                for msg in self.messager.get_message():
                    self.bridge.message_list.append(utils.decode_ints(msg[6::], 4))
                    text = utils.parse_text_message(msg, 4)
                    self.bridge.new_message_signal.emit("Serveur", text)

app = QApplication(sys.argv)
window = App()
window.show()
sys.exit(app.exec())