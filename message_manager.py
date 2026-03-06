import utils

class Frame():

    def __init__(self, header, type, length, message):
        self.header = header
        self.type = type
        self.length = length
        self.message = message
    