import cli, connection_manager, utils, message_manager



class MessageHandler:

    def __init__(self, client, bytes_per_char=4):
        self.client = client
        self.buffersize = 1024
        self.encoded_data = b''

    def add_data(self, data):
        self.encoded_data += data

    def get_message(self):
        ret = []
        while len(self.encoded_data) >= 6: #tant que le buffer n'a pas assez de bytes pour que ce soit une frame valide
            if not self.encoded_data.startswith(b'ISC'): #on jette un byte jusqu'au delimiteur
                self.encoded_data = self.encoded_data[1::]
                continue
            msg_type = self.encoded_data[3:4]
            if msg_type == b's' or msg_type == b't': #type: serveur ou texte
                N = int.from_bytes(self.encoded_data[4:6], byteorder='big')
                frame_length = 6 + (N * 4)
            elif msg_type == b'i': #type: image
                width = self.encoded_data[4] 
                height = self.encoded_data[5]
                frame_length = 6 + (width * height * 3)
            else: #type: inconnu
                self.encoded_data = self.encoded_data[3:]
                continue

            if len(self.encoded_data) >= frame_length: #Si le buffer contient au moins une frame
                message = self.encoded_data[:frame_length]
                ret.append(message)
                self.encoded_data = self.encoded_data[frame_length:] #on nettoie le buffer du message qu'on vient d'extraire
            else:
                break
        return ret #liste de messages ISC
    def afficher_messages(self):
        messages = self.get_message()
        for m in messages:
            print('[serveur] ' + utils.parse_text_message(m, 4))
    