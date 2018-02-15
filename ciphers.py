import random
import string


class Cipher:
    """Main class from which inherit all ciphers. It has two abstracs methods
    which will implemented by each subclass and three classmethods.
    One that includes a new level of encryption using a one time pad.
    Two other methods that split or join the text to show it in blocks of five.
    """
    def encrypt(self):
        """Encryption method to be implemented on each cipher."""
        raise NotImplementedError()

    def decrypt(self):
        """Decryption method to be implemented on each cipher."""
        raise NotImplementedError()

    @classmethod
    def pad_encryption(cls, pad, text, encryption=True):
        """Takes three arguments, one by default, to add another level of
        encryption to one of the ciphers used:
        - Pad is a numeric integer key that will be used to encrypt
        - Text is the message that is going to be encrypted or decrypted
        - Encryption takes True by default, so this method uses the pad to
        encrypt the text. If set to False it reverse the encryption to get
        the text decrypted.
        """
        num = len(text) // len(pad)
        rest = len(text) % len(pad)
        pad = pad * num + pad[:rest]

        DICT = string.ascii_uppercase * 2

        output = []
        for pos, char in enumerate(text):
            try:
                value_char = DICT.index(char)
            except ValueError:
                output.append(char)
            else:
                if encryption:
                    output.append(DICT[value_char+int(pad[pos])])
                else:
                    output.append(DICT[value_char-int(pad[pos])])
        return ''.join(output)

    @classmethod
    def split_in_blocks(cls, text):
        """Takes one argument, text, and split it in blocks of five, using
        some random special symbols to replace both spaces and the last block
        of characters if it doesn't get to be five.
        """
        symbols = ['@', '#', '$', '%', '&']

        # This num represent the characters needed to fill the last group of 5
        add = 5 - (len(text) % 5)

        output = []
        for letter in text:
            if letter == ' ':
                output.append(random.choice(symbols))
            else:
                output.append(letter)
        for num in range(add):
            output.append(random.choice(symbols))

        text = ''.join(output)

        output = []
        for index, letter in enumerate(text):
            if (index+1) % 5 == 0:
                output.append(letter + ' ')
            else:
                output.append(letter)
        return ''.join(output)

    @classmethod
    def join_from_blocks(cls, text):
        """Takes one argument, a text, and join it using some random symbols to
        represent the spaces between words in the original message.
        """
        symbols = ['@', '#', '$', '%', '&']

        text = ''.join(text.split())
        output = []
        for letter in text:
            if letter in symbols:
                output.append(' ')
            else:
                output.append(letter)
        return ''.join(output)
