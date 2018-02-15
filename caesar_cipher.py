import string

from ciphers import Cipher


class Caesar(Cipher):
    """Cipher that uses the Caesar encryption method to codify a message"""
    FORWARD = string.ascii_uppercase * 3

    def __init__(self, offset=3):
        """Initialize an instance of Caesar cipher with needed attributes"""
        self.offset = offset
        DICT = string.ascii_uppercase
        self.FORWARD = DICT + DICT[:self.offset+1]
        self.BACKWARD = DICT[:self.offset+1] + DICT

    def encrypt(self, text):
        """Takes a single argument (a text) and encrypt it using the
        Caesar encryption method.
        """
        output = []
        text = text.upper()
        for char in text:
            try:
                index = self.FORWARD.index(char)
            except ValueError:
                output.append(char)
            else:
                output.append(self.FORWARD[index+self.offset])
        return ''.join(output)

    def decrypt(self, text):
        """Takes a single argument (a caesar codified text) and decrypts it
        using the Caesar decryption method.
        """
        output = []
        text = text.upper()
        for char in text:
            try:
                index = self.BACKWARD.index(char)
            except ValueError:
                output.append(char)
            else:
                output.append(self.BACKWARD[index-self.offset])
        return ''.join(output)
