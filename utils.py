
BPC = 4

def int_to_bytes(value : int, num_bytes : int):
    return int(value).to_bytes(num_bytes, byteorder='big')

def bytes_to_int(data : bytes):
    return int.from_bytes(data, 'big')

def string_to_ints(text : str):
    result = []
    for char in text:
        char_bytes = char.encode('utf-8')
        char_int = int.from_bytes(char_bytes, byteorder='little')
        result.append(char_int)
    return result

def ints_to_string(int_list : list):
    result = ""
    for value in int_list:
        try:
            byte_length = max(1, (value.bit_length() + 7) // 8)
            char_bytes = value.to_bytes(byte_length, byteorder='little')
            result += char_bytes.decode('utf-8')
        except:
            result += "*"
    return result

def encode_ints(data : list, bytes_per_int : int):
    ret = b''
    for element in data:
        ret += (int_to_bytes(element,bytes_per_int))
    return ret

def decode_ints(data : list, bytes_per_int : int):
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
        ba += encode_ints(string_to_ints(c), bytes_per_char)
    return ba

def create_ints_message(ints, bytes_per_char):
    ba = ISC_HEADER + b's'
    ba += int_to_bytes(len(ints), 2)
    ba += encode_ints(ints, bytes_per_char)
    return ba

def parse_text_message(message, bytes_per_char):
    return ints_to_string(decode_ints(message[6::], bytes_per_char))

