import utils, random
from sympy import randprime

def encode_shift(t, key):
    key = int(key)
    encoded_text = []

    for c in t:
            encoded_text.append( c + key)
    return encoded_text

def decode_shift(encoded_text):
    
    frequent_words = ["le", "la","les","un","une","des", "et", "mais", "dans", "de", "d'", "ce", "ces"]
    possible_key = 1
    probable_key = {}
    while possible_key <= 30:
        key_try_tab = []
        for i in encoded_text:
            key_try_tab.append(i - possible_key)
        current_text = utils.ints_to_string(key_try_tab).lower()
        if  current_text.__contains__(' '):
            proba = 0
            for elements in frequent_words:
                if current_text.__contains__(elements):
                    proba += 1
            probable_key[possible_key] = proba
        possible_key += 1
    
    real_key = max(probable_key, key=probable_key.get)
    key_try_tab = []
    for i in encoded_text:
            key_try_tab.append(i - real_key)

    return real_key, key_try_tab

def encode_vigenere(text_ints, key_text):

    key_ints = utils.string_to_ints(key_text) 
    
    encoded_ints = []
    key_len = len(key_ints)
    
    for i in range(len(text_ints)):
        char_val = text_ints[i]
        key_val = key_ints[i % key_len]
        encoded_ints.append(char_val + key_val)
        
    return encoded_ints



def dh_private_key(max_val):
    return randprime(2, int(max_val))

def dh_halfkey(g, a, p):
    return pow(g, a, p)

def dh_shared_secret(B, a, p):
    return pow(B, a, p)



def is_prime(n):
   
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def get_primitive_root(p):
  
    if p == 2:
        return 1
    phi = p - 1
    factors = []
    d = 2
    temp = phi
    while d * d <= temp:
        if temp % d == 0:
            factors.append(d)
            while temp % d == 0:
                temp //= d
        d += 1
    if temp > 1:
        factors.append(temp)

    for g in range(2, p):
        is_root = True
        for q in factors:
            if pow(g, phi // q, p) == 1:
                is_root = False
                break
        if is_root:
            return g
    return None

def generate_custom_dh_space(user_limit):
    try:
        limit = int(user_limit)
    except:
        limit = 5000

    lower = int(limit * 0.2)
    if lower < 23:
        lower = 23

    for i in range(100):
        p = random.randint(lower, limit)
        if p % 2 == 0:
            p -= 1
        
        while p > lower:
            if is_prime(p):
                g = get_primitive_root(p)
                if g:
                    return p, g
            p -= 2
            
    return 23, 5
