from PySide6.QtCore import QObject, Signal
import html
import algos, utils

class UIBridge(QObject):
    new_message_signal = Signal(str, str)

    def __init__(self, ui, client, messager):
        super().__init__()
        self.ui = ui
        self.client = client
        self.messager = messager
        self.message_list = []
        self.encrypted_buffer = []
        
        self.new_message_signal.connect(self.display_new_message)
        self.setup_connections()

    def setup_connections(self):
        self.ui.shift_encode_fill_pushButton.clicked.connect(self.copy_last_message_shift_encode)
        self.ui.shift_encryption_pushButton.clicked.connect(self.handle_shift_encode)
        self.ui.shift_encode_send_encrypt_pushButton.clicked.connect(self.send_shift_encrypted)
        self.ui.Shift_decode_Decrypt_text_Pushbutton.clicked.connect(self.handle_shift_decode)
        self.ui.shift_decode_send_pushbutton.clicked.connect(self.send_shift_decode_key)
        self.ui.vigenere_fill_pushbutton.clicked.connect(self.copy_last_message_vigenere_encode)
        self.ui.vigenere_encode_encrypt_button.clicked.connect(self.handle_vigenere_encode)
        self.ui.vigenere_encode_send_pushbutton.clicked.connect(self.send_vigenere_encrypted)
        self.ui.dh_generate_modulo.clicked.connect(self.handle_dh_modular_world)
        self.ui.dh_generate_secret.clicked.connect(self.handle_dh_gen_priv)
        self.ui.dh_compute_halfkey.clicked.connect(self.handle_dh_compute_pub)
        self.ui.dh_compute_secret.clicked.connect(self.handle_dh_mutual_secret)
        self.ui.chat_send_pushButton.clicked.connect(self.handle_send_chat)

    def copy_last_message_shift_encode(self):
        try:
            to_set = utils.ints_to_string(self.message_list[-1])
            self.ui.shift_encode_text_lineEdit.setText(to_set)
        except IndexError:
            self.display_new_message("Error", "No message to be copied")
    def handle_shift_encode(self):
        try:
            to_encrypt = utils.string_to_ints(self.ui.shift_encode_text_lineEdit.text())
            key = self.ui.shift_encode_key_lineEdit.text()
            self.encrypted_buffer = algos.encode_shift(to_encrypt, int(key))
            self.ui.shift_encode_encrypt_lineEdit.setText(utils.ints_to_string(self.encrypted_buffer))
        except ValueError:
            self.display_new_message("Error", "No message or no key to start encryption")
    def send_shift_encrypted(self):
        try:
            if not self.encrypted_buffer:
                self.display_new_message("Error", "No encrypted message to send")
                return
            payload = utils.create_ints_message(self.encrypted_buffer,4)
            self.encrypted_buffer.clear
            self.ui.shift_encode_text_lineEdit.clear()
            self.ui.shift_encode_key_lineEdit.clear()
            self.ui.shift_encode_encrypt_lineEdit.clear()
            self.client.send_raw(payload)
        except ValueError:
            self.display_new_message("Error", "No encrypted message")

    def handle_shift_decode(self):
        try:
            key, decrypted = algos.decode_shift(self.message_list[-1])
            self.ui.shift_decode_key_lineEdit.setText(str(key))
            self.display_new_message("Decrypted", utils.ints_to_string(decrypted))
        except ValueError:
            self.display_new_message("Error", "No message to be decrypted")
    def send_shift_decode_key(self):
        try:
            if not self.ui.shift_decode_key_lineEdit.text():
                self.display_new_message("Error", "No encrypted message to send")
                return
            self.client.send(["-s", self.ui.shift_decode_key_lineEdit.text()])
            self.ui.shift_decode_key_lineEdit.clear()
        except ValueError:
            self.display_new_message("Error", "No key to send")

    def copy_last_message_vigenere_encode(self):
        try:
            to_set = utils.ints_to_string(self.message_list[-1])
            self.ui.vigenere_encode_text_editline.setText(to_set)
        except IndexError:
            self.display_new_message("Error", "No message to be copied")

    def handle_vigenere_encode(self):
        try:
            to_encrypt = utils.string_to_ints(self.ui.vigenere_encode_text_editline.text())
            key = self.ui.vigenere_encode_key_editline.text()
            self.encrypted_buffer = algos.encode_vigenere(to_encrypt, key)
            self.ui.vigenere_encode_encrypted_text_editline.setText(utils.ints_to_string(self.encrypted_buffer))
        except ValueError:
            self.display_new_message("Error", "No message or no key to start encryption")
    def send_vigenere_encrypted(self):
        try:
            if not self.encrypted_buffer:
                self.display_new_message("Error", "No encrypted message to send")
                return
            payload = utils.create_ints_message(self.encrypted_buffer,4)
            self.encrypted_buffer.clear
            self.ui.vigenere_encode_text_editline.clear()
            self.ui.vigenere_encode_key_editline.clear()
            self.ui.vigenere_encode_encrypted_text_editline.clear()
            self.client.send_raw(payload)
        except ValueError:
            self.display_new_message("Error", "No encrypted message")
    def handle_dh_modular_world(self):
        p, g = algos.generate_custom_dh_space(int(self.ui.dh_max_random_modulo.text()))
        self.ui.dh_modular_world.setText(str(p))
        self.ui.dh_generator.setText(str(g))
    def handle_dh_gen_priv(self):
        priv_a = algos.dh_private_key(int(self.ui.dh_modular_world.text()))
        self.ui.dh_private_A.setText(str(priv_a))
    def handle_dh_compute_pub(self):
        try:
            p = int(self.ui.dh_modular_world.text())
            g = int(self.ui.dh_generator.text())
            a = int(self.ui.dh_private_A.text())
            
            A = algos.dh_halfkey(g, a, p)
            self.ui.dh_public_A.setText(str(A))
        except ValueError:
            self.display_new_message("Error", "Wrong parameters P, G and Private Key")
    def handle_dh_mutual_secret(self):
        mutual_secret = algos.dh_shared_secret(int(self.ui.dh_public_B.text()), int(self.ui.dh_private_A.text()),int(self.ui.dh_modular_world.text()))
        self.ui.dh_mutual_secret.setText(str(mutual_secret))

    def handle_send_chat(self):
        text = self.ui.chat_lineEdit.text()
        if text:
            if self.ui.chat_checkBox.isChecked():
                self.client.send(["-s", text])
            else:
                self.client.send([text])
            self.ui.chat_lineEdit.clear()

    def display_new_message(self, msg_type, content):
        safe_content = html.escape(content)
        color = "#2ecc71" if msg_type == "serveur" else "#bb0000"
        formatted_text = f'<b style="color:{color}">[{msg_type}]</b> {safe_content}'
        self.ui.textBrowser.append(formatted_text)