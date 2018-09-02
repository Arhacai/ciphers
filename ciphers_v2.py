import random
import string


class Cipher:
    """
    Main class from which inherit all ciphers. It has two abstracs methods
    which will implemented by each subclass and three classmethods.
    One that includes a new level of encryption using a one time pad.
    Two other methods that split or join the text to show it in blocks of five.
    """

    ASCII_DICT = string.ascii_uppercase

    def __init__(self, pad='', in_blocks=False):
        self.pad = pad
        self.in_blocks = in_blocks

    def encrypt(self, message):
        """Encryption method to be implemented on each cipher."""
        raise NotImplementedError()

    def decrypt(self, message):
        """Decryption method to be implemented on each cipher."""
        raise NotImplementedError()

    def pad_encryption(self, message, encrypt=True):
        """
        Takes three arguments, one by default, to add another level of
        encryption to one of the ciphers used:
        - Pad is a numeric integer key that will be used to encrypt
        - Message is the text that is going to be encrypted or decrypted
        - Encryption is set to True by default, so this method uses the pad to
        encrypt the text. If set to False it reverse the encryption to get
        the text decrypted.
        """

        if self.pad == '':
            return message

        num = len(message) // len(self.pad)
        rest = len(message) % len(self.pad)
        pad = self.pad * num + self.pad[:rest]

        letters = self.ASCII_DICT * 2

        output = []
        for pos, char in enumerate(message):
            try:
                letter = letters.index(char)
            except ValueError:
                output.append(char)
            else:
                if encrypt:
                    output.append(letters[letter + int(pad[pos])])
                else:
                    output.append(letters[letter - int(pad[pos])])
        return ''.join(output)

    def split_in_blocks(self, message):
        """
        Takes one argument, text, and split it in blocks of five, using
        some random special symbols to replace both spaces and the last block
        of characters if it doesn't get to be five.
        """

        if not self.in_blocks:
            return message

        symbols = ['@', '#', '$', '%', '&']

        # This num represent the characters needed to fill the last group of 5
        add = 5 - (len(message) % 5)

        output = []
        for letter in message:
            if letter == ' ':
                output.append(random.choice(symbols))
            else:
                output.append(letter)
        for num in range(add):
            output.append(random.choice(symbols))

        message = ''.join(output)

        output = []
        for index, letter in enumerate(message):
            if (index + 1) % 5 == 0:
                if (index + 1) == len(message):
                    output.append(letter)
                else:
                    output.append(letter + ' ')
            else:
                output.append(letter)
        return ''.join(output)

    def join_from_blocks(self, message):
        """
        Takes one argument, a text, and join it using some random symbols to
        represent the spaces between words in the original message.
        """

        if not self.in_blocks:
            return message

        symbols = ['@', '#', '$', '%', '&']

        message = ''.join(message.split())
        output = []
        for letter in message:
            if letter in symbols:
                output.append(' ')
            else:
                output.append(letter)
        while output[-1] == ' ':
            del output[-1]

        return ''.join(output)


class Affine(Cipher):
    """
    Cipher that uses the Affine encryption method to codify a message.
    This method will require two inputs from user:
    - A first numeric key from a list of valid numbers.
    - A second numeric key as any positive non zero integers.
    """

    ALPHA = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
    ALPHA_INV = [1, 9, 21, 15, 3, 19, 7, 23, 11, 5, 17, 25]

    def __init__(self, pad='', in_blocks=False):
        """Initialize an instance of Affine cipher with needed attributes"""
        super().__init__(pad, in_blocks)
        self.alpha, self.alpha_inv = self.get_alpha()
        self.beta = self.get_beta()

    def encrypt(self, message):
        """
        Takes a single argument (a text) and encrypts it using the
        Affine encryption method.
        """
        positions = []
        message = message.upper()
        for char in message:
            try:
                index = self.ASCII_DICT.index(char)
                positions.append(index)
            except ValueError:
                positions.append(char)
        for index, num in enumerate(positions):
            if isinstance(positions[index], int):
                positions[index] = (num*self.alpha + self.beta) % 26

        output = []
        for num in positions:
            if isinstance(num, int):
                output.append(self.ASCII_DICT[num])
            else:
                output.append(num)
        return self.split_in_blocks(self.pad_encryption(''.join(output)))

    def decrypt(self, message):
        """
        Takes a single argument (an affine codified text) and decrypts it
        using the Affine decryption method.
        """

        positions = []
        message = self.join_from_blocks(message.upper())
        for char in message:
            try:
                index = self.ASCII_DICT.index(char)
                positions.append(index)
            except ValueError:
                positions.append(char)
        for index, num in enumerate(positions):
            if isinstance(positions[index], int):
                positions[index] = (self.alpha_inv * (num - self.beta)) % 26

        output = []
        for num in positions:
            if isinstance(num, int):
                output.append(self.ASCII_DICT[num])
            else:
                output.append(num)
        return self.pad_encryption(''.join(output), False)

    def get_alpha(self):
        while True:
            key = input("Choose the first key from this list: {}\n"
                        "Or leave blank for default(5)>").format(self.ALPHA)
            if key == '':
                return 5, 21
            else:
                try:
                    alpha = int(key)
                except ValueError:
                    print("Sorry, you must choose a valid key.")
                else:
                    if alpha in self.ALPHA:
                        index = self.ALPHA.index(alpha)
                        alpha_inv = self.ALPHA_INV[index]
                        return alpha, alpha_inv
                    else:
                        print("Sorry, you must choose a valid key.")

    def get_beta(self):
        while True:
            key = input("Choose a second numeric key. "
                        "Leave blank for default (8)> ")
            if key == '':
                return 8
            else:
                try:
                    return int(key)
                except ValueError:
                    print(
                        "Sorry, you must choose a valid positive integer key"
                    )


class Caesar(Cipher):
    """Cipher that uses the Caesar encryption method to codify a message"""

    def __init__(self, pad='', in_blocks=False, offset=3):
        """Initialize an instance of Caesar cipher with needed attributes"""
        super().__init__(pad, in_blocks)
        self.offset = offset
        self.FORWARD = self.ASCII_DICT + self.ASCII_DICT[:self.offset+1]
        self.BACKWARD = self.ASCII_DICT[:self.offset+1] + self.ASCII_DICT

    def encrypt(self, message):
        """Takes a single argument (a text) and encrypt it using the
        Caesar encryption method.
        """
        output = []
        message = message.upper()
        for char in message:
            try:
                index = self.FORWARD.index(char)
            except ValueError:
                output.append(char)
            else:
                output.append(self.FORWARD[index+self.offset])
        return self.split_in_blocks(self.pad_encryption(''.join(output)))

    def decrypt(self, message):
        """Takes a single argument (a caesar codified text) and decrypts it
        using the Caesar decryption method.
        """
        output = []
        message = self.join_from_blocks(message.upper())
        for char in message:
            try:
                index = self.BACKWARD.index(char)
            except ValueError:
                output.append(char)
            else:
                output.append(self.BACKWARD[index-self.offset])
        return self.pad_encryption(''.join(output), False)
