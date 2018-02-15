import string

from ciphers import Cipher


class Affine(Cipher):
    """Cipher that uses the Affine encryption method to codify a message.
    This method will require two inputs from user:
    - A first numeric key from a list of valid numbers.
    - A second numeric key as any positive non zero integers.
    """
    ALPHA = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
    ALPHA_INV = [1, 9, 21, 15, 3, 19, 7, 23, 11, 5, 17, 25]

    def __init__(self):
        """Initialize an instance of Affine cipher with needed attributes"""
        self.ORDERED = string.ascii_uppercase
        self.get_keys()

    def encrypt(self, text):
        """Takes a single argument (a text) and encrypts it using the
        Affine encryption method.
        """
        positions = []
        text = text.upper()
        for char in text:
            try:
                index = self.ORDERED.index(char)
                positions.append(index)
            except ValueError:
                positions.append(char)
        for index, num in enumerate(positions):
            if isinstance(positions[index], int):
                positions[index] = (num*self.alpha + self.beta) % 26

        output = []
        for num in positions:
            if isinstance(num, int):
                output.append(self.ORDERED[num])
            else:
                output.append(num)
        return ''.join(output)

    def decrypt(self, text):
        """Takes a single argument (an affine codified text) and decrypts it
        using the Affine decryption method.
        """
        positions = []
        text = text.upper()
        for char in text:
            try:
                index = self.ORDERED.index(char)
                positions.append(index)
            except ValueError:
                positions.append(char)
        for index, num in enumerate(positions):
            if isinstance(positions[index], int):
                positions[index] = (self.alpha_inv * (num - self.beta)) % 26

        output = []
        for num in positions:
            if isinstance(num, int):
                output.append(self.ORDERED[num])
            else:
                output.append(num)
        return ''.join(output)

    def get_keys(self):
        """Gets from users the two needed key values to encrypt the message:
        - First key value must be one from a list provided and uses the
        value of 5 if no one provided.
        - Second key value can be any positive non zero integer
        """
        while True:
            print("""
Choose the first key from this list: {}\n""".format(self.ALPHA))

            try:
                key_a = input("Or leave blank for default(5)> ")
                if key_a == '':
                    self.alpha = 5
                    self.alpha_inv = 21
                    break
                if int(key_a) in self.ALPHA:
                    self.alpha = int(key_a)
                    index = self.ALPHA.index(int(key_a))
                    self.alpha_inv = self.ALPHA_INV[index]
                    break
            except ValueError:
                print("Sorry, you must choose a valid key.")
            else:
                print("Sorry, you must choose a valid key.")

        while True:
            try:
                key_b = input("""
Choose a second numeric key. Leave blank for default (8)> """)
                if key_b == '':
                    self.beta = 8
                    break
                if int(key_b) > 0:
                    self.beta = int(key_b)
                    break
            except ValueError:
                print("Sorry, you must choose a valid positive integer key")
            else:
                print("Sorry, you must choose a valid positive integer key")
