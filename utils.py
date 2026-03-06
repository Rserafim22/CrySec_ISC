import message_manager

BPC = 4

def int_to_bytes(value, num_bytes):
    return value.to_bytes(num_bytes, byteorder='big')

def bytes_to_int(data):
    return int.from_bytes(data, 'big')

def string_to_ints(text):
    ret = []
    for c in text:
        ret.append(ord(c)) #ord : transforme char en sa valeur ascii
    return ret

def ints_to_string(int_list): #verifier la validation !!!!!!
    ret = ''
    for integer in int_list: 
        if integer >= 0 and integer <= 255: #utf-8 : char sur 8 bits
            ret += chr(integer) #chr: donne le char correspondant a la valeur ascii
        else:
            ret += '*'
    return ret

def encode_ints(data, bytes_per_int):
    ret = b''
    for element in data:
        ret += (int_to_bytes(element,bytes_per_int))
    return ret

def decode_ints(data, bytes_per_int):
    ret = []
    for i in range(0, len(data), bytes_per_int):
        chunk = data[i : i + bytes_per_int]
        ret.append(bytes_to_int(chunk))
    return ret

ISC_HEADER = b'ISC'

def create_text_message(text, bytes_per_char, for_server=False):
    ba = ISC_HEADER
    if for_server:
        ba += b's'
    else:
        ba += b't'

    ba += int_to_bytes(len(text), 2)
    for c in text:
        ba += encode_ints(string_to_ints(c),bytes_per_char)
    return ba

def creat_image_message(width, height,image_data):
    pass

def parse_text_message(message, bytes_per_char):
    return ints_to_string(decode_ints(message[6::], bytes_per_char))
    
def debug_binary(packet):
    print("--- Analyse Binaire Complète du Paquet ---")
    
    # 1. Header 'ISC' (Bytes 0 à 2)
    header = packet[0:3]
    print(f"Header  (ISC) : {' '.join(f'{b:08b}' for b in header)}")
    
    # 2. Type (Byte 3)
    msg_type = packet[3:4]
    print(f"Type     ({msg_type.decode()}) : {packet[3]:08b}")
    
    # 3. Longueur (Bytes 4 et 5) - Valeur N * 4 attendue par le serveur
    longueur_val = int.from_bytes(packet[4:6], byteorder='big')
    print(f"Length   ({longueur_val}) : {' '.join(f'{b:08b}' for b in packet[4:6])}")
    
    # 4. Payload : Analyse de tous les caractères (4 octets par char)
    # On commence à l'index 6 jusqu'à la fin du paquet
    payload = packet[6:]
    bytes_per_char = 4
    
    print(f"--- Contenu ({len(payload)} bytes) ---")
    for i in range(0, len(payload), bytes_per_char):
        char_bytes = payload[i : i + bytes_per_char]
        char_val = int.from_bytes(char_bytes, byteorder='big')
        
        # On essaie d'afficher le caractère ASCII pour que ce soit lisible
        try:
            char_label = chr(char_val) if 32 <= char_val <= 126 else "?"
        except:
            char_label = "?"
            
        binary_str = ' '.join(f'{b:08b}' for b in char_bytes)
        print(f"Char {i//4 + 1} ('{char_label}') : {binary_str}")


