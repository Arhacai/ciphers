import random
import string


class Cipher:
    """
    Main class from which inherit all ciphers. It has two abstracs methods
    which will implemented by each subclass and three classmethods.
    One that includes a new level of encryption using a one time pad.
    Two other methods that split or join the text to show it in blocks of five.
    """

    LETTERS = string.ascii_uppercase

    def __init__(self, pad='', in_blocks=False):
        self.pad = pad
        self.in_blocks = in_blocks

    def encrypt(self, text):
        """Encryption method to be implemented on each cipher."""
        raise NotImplementedError()

    def decrypt(self, text):
        """Decryption method to be implemented on each cipher."""
        raise NotImplementedError()

    def pad_encryption(self, text, encrypt=True):
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
            return text

        num = len(text) // len(self.pad)
        rest = len(text) % len(self.pad)
        pad = self.pad * num + self.pad[:rest]

        letters = self.LETTERS * 2

        output = []
        for pos, char in enumerate(text):
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

    def split_in_blocks(self, text):
        """
        Takes one argument, text, and split it in blocks of five, using
        some random special symbols to replace both spaces and the last block
        of characters if it doesn't get to be five.
        """

        if not self.in_blocks:
            return text

        symbols = ['@', '#', '$', '%', '&']

        # This num represent the characters needed to fill the last group of 5
        add = 5 - (len(text) % 5)

        output = []
        for letter in text:
            if letter == ' ':
                output.append(random.choice(symbols))
            else:
                output.append(letter)
        if add != 5:
            for num in range(add):
                output.append(random.choice(symbols))
        text = ''.join(output)

        output = []
        for index, letter in enumerate(text):
            if (index + 1) % 5 == 0:
                if (index + 1) == len(text):
                    output.append(letter)
                else:
                    output.append(letter + ' ')
            else:
                output.append(letter)
        return ''.join(output)

    def join_from_blocks(self, text):
        """
        Takes one argument, a text, and join it using some random symbols to
        represent the spaces between words in the original message.
        """

        if not self.in_blocks:
            return text

        symbols = ['@', '#', '$', '%', '&']

        text = ''.join(text.split())
        output = []
        for letter in text:
            if letter in symbols:
                output.append(' ')
            else:
                output.append(letter)
        while output[-1] == ' ':
            del output[-1]

        return ''.join(output)

    def encode(self, message):
        return self.split_in_blocks(
            self.pad_encryption(
                self.encrypt(message)
            )
        )

    def decode(self, message):
        return self.decrypt(
            self.pad_encryption(
                self.join_from_blocks(message), False
            )
        )


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

    def encrypt(self, text):
        """
        Takes a single argument (a text) and encrypts it using the
        Affine encryption method.
        """
        positions = []
        text = text.upper()
        for char in text:
            try:
                index = self.LETTERS.index(char)
                positions.append(index)
            except ValueError:
                positions.append(char)
        for index, num in enumerate(positions):
            if isinstance(positions[index], int):
                positions[index] = (num*self.alpha + self.beta) % 26

        output = []
        for num in positions:
            if isinstance(num, int):
                output.append(self.LETTERS[num])
            else:
                output.append(num)
        return ''.join(output)

    def decrypt(self, text):
        """
        Takes a single argument (an affine codified text) and decrypts it
        using the Affine decryption method.
        """
        positions = []
        text = text.upper()
        for char in text:
            try:
                index = self.LETTERS.index(char)
                positions.append(index)
            except ValueError:
                positions.append(char)
        for index, num in enumerate(positions):
            if isinstance(positions[index], int):
                positions[index] = (self.alpha_inv * (num - self.beta)) % 26

        output = []
        for num in positions:
            if isinstance(num, int):
                output.append(self.LETTERS[num])
            else:
                output.append(num)
        return ''.join(output)

    def get_alpha(self):
        while True:
            key = input("Choose a first key from this list: {}\n"
                        "Or leave blank for default(5)> ".format(self.ALPHA))
            if key == '':
                return 5, 21
            try:
                alpha = int(key)
            except ValueError:
                print("Sorry, you must choose a valid key.\n")
            else:
                if alpha in self.ALPHA:
                    index = self.ALPHA.index(alpha)
                    alpha_inv = self.ALPHA_INV[index]
                    return alpha, alpha_inv
                print("Sorry, you must choose a valid key.\n")

    def get_beta(self):
        while True:
            key = input("Choose a second positive numeric key. "
                        "Leave blank for default (8)> ")
            if key == '':
                return 8
            try:
                beta = int(key)
            except ValueError:
                print("Sorry, key must be a positive integer\n")
            else:
                if beta > 0:
                    return beta
                print("Sorry, key must be a positive integer\n")


class Atbash(Cipher):
    """
    Cipher that uses the Atbash encryption method to codify a message
    """

    def __init__(self, pad='', in_blocks=False):
        """Initialize an instance of Atbash cipher with needed attributes"""
        super().__init__(pad, in_blocks)
        self.ORDERED = self.LETTERS
        self.REVERSED = self.ORDERED[::-1]

    def encrypt(self, text):
        """
        Takes a single argument (a text) and encrypts it using the
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
        """
        Takes a single argument (an atbash codified text) and decrypts it
        using the Atbash decryption method.
        """
        return self.encrypt(text)


class Caesar(Cipher):
    """
    Cipher that uses the Caesar encryption method to codify a message
    """

    def __init__(self, pad='', in_blocks=False, offset=3):
        """Initialize an instance of Caesar cipher with needed attributes"""
        super().__init__(pad, in_blocks)
        self.offset = offset
        self.FORWARD = self.LETTERS + self.LETTERS[:self.offset+1]
        self.BACKWARD = self.LETTERS[:self.offset+1] + self.LETTERS

    def encrypt(self, text):
        """
        Takes a single argument (a text) and encrypt it using the
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
        """
        Takes a single argument (a caesar codified text) and decrypts it
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


class Keyword(Cipher):
    """Cipher that uses the Keyword encryption method to codify a message
    This method will require one input from user, a keyword, to code message.
    """

    def __init__(self, pad='', in_blocks=False):
        """Initialize an instance of Keyword cipher with needed attributes"""
        super().__init__(pad, in_blocks)
        self.ORDERED = string.ascii_uppercase
        self.ENCRYPTED = self.get_encrypted_dict()

    def encrypt(self, text):
        """
        Takes a single argument (a text) and encrypts it using the
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
        """
        Takes a single argument (a keyword codified text) and decrypts it
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
        """
        Gets an alphanumeric keyword from user.
        If not provided, it uses 'kryptos' as default keyword,
        """
        key = input(
            "Use you're own keyword or leave blank for default (krypthos): "
        ).upper()

        if key == '':
            return 'KRYPTHOS'
        return self.clean_keyword(key)

    def clean_keyword(self, keyword):
        """
        Removes any character repeated and spaces from the key provided.
        """
        key = []
        for letter in keyword:
            if letter not in key and letter != ' ':
                key.append(letter)
        return ''.join(key)

    def get_encrypted_dict(self):
        """
        Creates an encrypted dictionary with the keyword provided by the
        user, following the rules of the Keyword Cipher method.
        """
        encrypted_dict = self.get_keyword()

        for letter in self.ORDERED:
            if letter not in encrypted_dict:
                encrypted_dict += letter
        return encrypted_dict
