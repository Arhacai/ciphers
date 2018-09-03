import ciphers_v2
import os


def clear_screen():
    """Clear the screen to prepare it to show the menu."""
    os.system('cls' if os.name == 'nt' else 'clear')


def show_menu():
    """Shows the main menu of Secret Messages program."""
    clear_screen()
    print("""

This is the Secret Messages project for the Treehouse Techdegree.

These are the current availables ciphers:

-Caesar
-Atbash
-Affine
-Keyword

Enter QUIT to exit Secret Messages.

""")


def get_cipher():
    """Prompt a message to the user to choose one of the available ciphers."""
    available_ciphers = ['Caesar', 'Atbash', 'Affine', 'Keyword']
    module = __import__('ciphers_v2')

    while True:
        cipher = input("Which cipher would you like to use? ").lower().capitalize()
        if cipher == 'Quit':
            return False
        if cipher in available_ciphers:
            return getattr(module, cipher)
        print("Sorry, that's not a valid cipher.\n")


def get_message():
    """Prompts a message on screen to request a message from user."""
    message = input("\nThat's an excellent cipher. What's the message? ")
    return message


def get_option():
    """Asks the user if wants to encrypt or decrypt the message."""
    while True:
        try:
            option = input("\nAre we going to encode or decode? ")
            if option == 'encode' or option == 'decode':
                return option
            else:
                raise ValueError
        except ValueError:
            print("Sorry, you have to enter a valid command.")


def get_pad():
    """Let the user to use a new level of encryption with a one time pad key.
    This key must be an integer.
    """
    while True:
        pad = (input("\nEnter a pad number (leave blank for no pad): "))
        if pad == '':
            return pad
        else:
            try:
                return str(int(pad))
            except ValueError:
                print("\nSorry, you have to enter a valid numeric key pad")


def in_blocks():
    """Let the user to encrypt the message in blocks of five characters.
    By default is set to NO.
    """
    option = input("\nEncryption in blocks of 5? y/N> ").lower()
    if option == 'y':
        return True
    else:
        return False


def cipher_again():
    """Ask the user if wants to encrypt or decrypt another message or exit
    the program. By default the answer is NO.
    """
    start = input("\nDo you want to encrypt or decrypt another message [Y/n]")
    if start.lower() != 'n':
        main()
    else:
        print("\nThanks for using this Secret Messages project. Bye bye!")


def main():
    """Main function of Secret Messages. Runs the main program."""
    show_menu()
    cipher = get_cipher()
    if cipher:
        message = get_message()
        option = get_option()
        #cipher(get_pad(), in_blocks()).get_option()(message)
        cipher_again()
    else:
        print("\nThanks for using this Secret Messages project. Bye bye!")


if __name__ == '__main__':
    main()
