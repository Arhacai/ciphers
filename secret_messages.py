import os
import random
import string
import time


def clear_screen():
    """Clear the screen to prepare it to show the menu."""
    os.system('cls' if os.name == 'nt' else 'clear')


class VisualDecoder:
    LETTERS = string.ascii_uppercase + " !$%&?¿¡@#"
    start = 0

    def __init__(self, text1, text2):
        self.text1 = list(text1)
        self.text2 = list(text2)

    def suffle(self,):
        for index in range(self.start, len(self.text1)):
            self.text1[index] = random.choice(self.LETTERS)

    def transform(self):
        self.suffle()
        if self.text1[self.start] == self.text2[self.start]:
            self.start += 1
        print(''.join(self.text1))
        time.sleep(0.02)

    def run(self):
        while self.text1 != self.text2:
            clear_screen()
            self.transform()
        clear_screen()
        print("You're decoded message is: ")
        print(''.join(self.text1))


def show_menu():
    """Shows the main menu of Secret Messages program."""
    clear_screen()
    print(
        "This is the Secret Messages project for the Treehouse Techdegree.\n\n"
        "These are the current availables ciphers:\n\n"
        "-Caesar\n"
        "-Atbash\n"
        "-Affine\n"
        "-Keyword\n\n"
        "Enter QUIT to exit Secret Messages.\n\n"
    )


def get_cipher_or_quit():
    """Prompts a message to the user to choose one of the available ciphers."""
    available_ciphers = ['Caesar', 'Atbash', 'Affine', 'Keyword']
    module = __import__('ciphers')

    while True:
        cipher = input(
            "Which cipher would you like to use? ").lower().capitalize()
        if cipher == 'Quit':
            return False
        if cipher in available_ciphers:
            pad = get_pad()
            blocks = in_blocks()
            return getattr(module, cipher)(pad, blocks)
        print("Sorry, that's not a valid cipher.\n")


def get_message():
    """Prompts a message on screen to request a message from user."""
    message = input("What's the message? ")
    return message


def get_option():
    """
    Asks the user if wants to encrypt or decrypt the message and returns
    the option as a string to call the proper method of the cipher instance
    """
    while True:
        try:
            option = input("Are we going to encode or decode? ")
            if option == 'encode' or option == 'decode':
                return option
            else:
                raise ValueError
        except ValueError:
            print("Sorry, you have to enter a valid command.\n")


def get_pad():
    """
    Lets the user to use a new level of encryption with a one time pad key.
    This key must be an integer.
    """
    while True:
        pad = (input("Enter a pad number (leave blank for no pad): "))
        if pad == '':
            return pad
        else:
            try:
                return str(int(pad))
            except ValueError:
                print("Sorry, you have to enter a valid numeric key pad\n")


def in_blocks():
    """
    Let the user to encrypt the message in blocks of five characters.
    By default is set to NO.
    """
    option = input("Encryption in blocks of 5? y/N> ").lower()
    if option == 'y':
        return True
    return False


def show_message(cipher, option, message):
    """
    Uses the option to call the proper method on the cipher instance and
    prints the encoded/decoded message on screen
    """
    result = getattr(cipher, option)(message)
    if option == 'decode':
        VisualDecoder(message, result).run()
    else:
        print("\nYour {}d message is: {}".format(option, result))


def cipher_again():
    """
    Ask the user if wants to encrypt or decrypt another message or exit
    the program. By default the answer is NO.
    """
    start = input("\nDo you want to encrypt or decrypt another message [Y/n]")
    if start.lower() != 'n':
        run()
    else:
        print("Thanks for using this Secret Messages project. Bye bye!")


def run():
    """Main function of Secret Messages. Runs the main program."""
    show_menu()
    cipher = get_cipher_or_quit()
    if cipher:
        message = get_message()
        option = get_option()
        show_message(cipher, option, message)
        cipher_again()
    else:
        print("Thanks for using this Secret Messages project. Bye bye!")


if __name__ == '__main__':
    run()
