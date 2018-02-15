import string

from ciphers import Cipher


class Keyword(Cipher):
    """Cipher that uses the Keyword encryption method to codify a message
    This method will require one input from user, a keyword, to code message.
    """

    def __init__(self):
        """Initialize an instance of Keyword cipher with needed attributes"""
        self.keyword = self.get_keyword()
        self.ORDERED = string.ascii_uppercase
        self.ENCRYPTED = self._set_encrypted_dict()

    def encrypt(self, text):
        """Takes a single argument (a text) and encrypts it using the
        Keyword encryption method.
        """
        output = []
        text = text.upper()
        for char in text:
            try:
                index = self.ORDERED.index(char)
            except ValueError:
                output.append(char)
            else:
                output.append(self.ENCRYPTED[index])
        return ''.join(output)

    def decrypt(self, text):
        """Takes a single argument (a keyword codified text) and decrypts it
        using the Keyword decryption method.
        """
        output = []
        text = text.upper()
        for char in text:
            try:
                index = self.ENCRYPTED.index(char)
            except ValueError:
                output.append(char)
            else:
                output.append(self.ORDERED[index])
        return ''.join(output)

    def get_keyword(self):
        """Gets an alphanumeric keyword from user.
        If not provided, it uses 'kryptos' as default keyword,
        """
        key = input("""
Use you're own keyword or leave blank for default (krypthos): """).upper()
        if key == '':
            return 'KRYPTHOS'
        else:
            return key

    def _correct_keyword(self, keyword):
        """Removes any character repeated and spaces from the key provided."""
        key = []
        for letter in keyword:
            if letter not in key and letter != ' ':
                key.append(letter)
        return ''.join(key)

    def _set_encrypted_dict(self):
        """Creates an encrypted dictionary with the keyword provided by the
        user, following the rules of the Keyword Cipher method.
        """
        encrypted_dict = self._correct_keyword(self.keyword)

        for letter in self.ORDERED:
            if letter not in encrypted_dict:
                encrypted_dict += letter
        return encrypted_dict
