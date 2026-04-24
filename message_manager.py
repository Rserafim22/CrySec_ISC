import utils



class MessageHandler:

    def __init__(self, client):
        self.client = client
        self.encoded_data = b''
        self.int_messages = []
        self.message_list = []
    

    def add_data(self, data):
        self.encoded_data += data

    def get_message(self):
        ret = []
        while len(self.encoded_data) >= 6:
            if not self.encoded_data.startswith(b'ISC'):
                self.encoded_data = self.encoded_data[1::]
                continue
            msg_type = self.encoded_data[3:4]
            if msg_type == b's' or msg_type == b't':
                N = int.from_bytes(self.encoded_data[4:6], byteorder='big')
                frame_length = 6 + (N * 4)
            else:
                self.encoded_data = self.encoded_data[3:]
                continue

            if len(self.encoded_data) >= frame_length:
                message = self.encoded_data[:frame_length]
                ret.append(message)
                self.encoded_data = self.encoded_data[frame_length:]
            else:
                break
        return ret 
    def afficher_messages(self):
        messages = self.get_message()
        message_list = ''
        for m in messages:
            self.int_messages.append(utils.decode_ints(m[6::], 4))
            print('[serveur] ' + '"' + utils.parse_text_message(m, 4) + '"')
            message_list += utils.parse_text_message(m, 4)
        return message_list
                       
        