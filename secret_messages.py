import affine_cipher
import atbash_cipher
import caesar_cipher
import keyword_cipher
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
    available_ciphers = ['CAESAR', 'ATBASH', 'AFFINE', 'KEYWORD']

    while True:
        cipher = input("Which cipher would you like to use? ").upper()
        if cipher == 'QUIT':
            return False

        if cipher in available_ciphers:
            if cipher == 'CAESAR':
                return caesar_cipher.Caesar()
            if cipher == 'ATBASH':
                return atbash_cipher.Atbash()
            if cipher == 'KEYWORD':
                return keyword_cipher.Keyword()
            if cipher == 'AFFINE':
                return affine_cipher.Affine()
            break
        else:
            print("Sorry, that's not a valid cipher.\n")


def get_message():
    """Prompts a message on screen to request a message from user."""
    message = input("\nThat's an excellent cipher. What's the message? ")
    return message


def get_option():
    """Asks the user if wants to encrypt or decrypt the message."""
    while True:
        try:
            options = ["encrypt", "e", "decrypt", "d"]
            option = input("\nAre we going to [e]ncrypt or [d]ecrypt? ")
            if option in options:
                return option
            else:
                raise ValueError
        except ValueError:
            print("Sorry, you have to enter a valid command.")
        else:
            break


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
            else:
                return pad


def in_blocks():
    """Let the user to encrypt the message in blocks of five characters.
    By default is set to NO.
    """
    option = input("\nEncryption in blocks of 5? y/N> ").lower()
    if option == 'y':
        return True
    else:
        return False


def encrypt_message(cipher, message):
    """Gets the message written by the user and all the options selected,
    aswell the cipher chosen, and prints the encrypted message on screen.
    """
    pad = get_pad()

    if pad == '':
        encrypted_message = cipher.encrypt(message)
        if in_blocks():
            print(cipher.split_in_blocks(encrypted_message))
        else:
            print(encrypted_message)
    else:
        encrypted_message = cipher.encrypt(message)
        pad_encrypted_message = cipher.pad_encryption(pad, encrypted_message)
        if in_blocks():
            print(cipher.split_in_blocks(pad_encrypted_message))
        else:
            print(pad_encrypted_message)


def decrypt_message(cipher, message):
    """Gets the encrypted message written by the user and all the options
    selected, aswell the cipher chosen, and prints the decrypted message
    on screen.
    """
    pad = get_pad()
    if pad == '':
        if in_blocks():
            joined_message = cipher.join_from_blocks(message)
            decrypted_message = cipher.decrypt(joined_message)
            print(decrypted_message)
        else:
            decrypted_message = cipher.decrypt(message)
            print(decrypted_message)
    else:
        if in_blocks():
            message = cipher.join_from_blocks(message)
            decrypted_message = cipher.pad_encryption(pad, message, False)
            pad_decrypted_message = cipher.decrypt(decrypted_message)
            print(pad_decrypted_message)
        else:
            decrypted_message = cipher.pad_encryption(pad, message, False)
            pad_decrypted_message = cipher.decrypt(decrypted_message)
            print(pad_decrypted_message)


def process_message(cipher, option, message):
    """Let the user select to encrypt or decrypt the message, once the option
    is valid, the message is processed. Takes three arguments:
    """
    if option.lower() == 'encrypt' or option.lower() == 'e':
        encrypt_message(cipher, message)

    if option.lower() == 'decrypt' or option.lower() == 'd':
        decrypt_message(cipher, message)


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
        process_message(cipher, option, message)
        cipher_again()
    else:
        print("\nThanks for using this Secret Messages project. Bye bye!")


if __name__ == '__main__':
    main()
