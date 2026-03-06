import message_manager


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
        print(element)
        ret += (int_to_bytes(element,bytes_per_int))
    return ret

def decode_ints(data, bytes_per_int):
    ret = []
    for i in range(0, len(data), bytes_per_int):
        chunk = data[i : i + bytes_per_int]
        ret.append(bytes_to_int(chunk))
    return ret

ISC_HEADER = b'ISC'

def create_text_message(text, bytes_per_char):
    ba = ISC_HEADER
    ba += b't'
    ba += int_to_bytes(len(text), 2)
    for c in text:
        ba += encode_ints(string_to_ints(c),bytes_per_char)
    return ba

test1 = int_to_bytes(120, 2)
print(test1)
test1 = bytes_to_int(test1)
print(test1)
test2 = string_to_ints('salut')
print(test2)
encode_ints(test2,2)
print(decode_ints(b'\x00\x00\x00\x41\x00\x00\x00\x42\x00\x00\x00\x43', 4))
##test2.append(234432423)
##test2 = ints_to_string(test2)
##print(test2)


