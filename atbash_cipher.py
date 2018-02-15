import string

from ciphers import Cipher


class Atbash(Cipher):
    """Cipher that uses the Atbash encryption method to codify a message"""

    def __init__(self):
        """Initialize an instance of Atbash cipher with needed attributes"""
        self.ORDERED = string.ascii_uppercase
        self.REVERSED = self.ORDERED[::-1]

    def encrypt(self, text):
        """Takes a single argument (a text) and encrypts it using the
        Atbash encryption method.
        """
        output = []
        text = text.upper()
        for char in text:
            try:
                index = self.ORDERED.index(char)
            except ValueError:
                output.append(char)
            else:
                output.append(self.REVERSED[index])
        return ''.join(output)

    def decrypt(self, text):
        """Takes a single argument (an atbash codified text) and decrypts it
        using the Atbash decryption method.
        """
        return self.encrypt(text)
