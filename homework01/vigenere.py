"""Implements Vigenere cipher for encryption and decryption"""


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    keyword = (keyword * ((len(plaintext) // len(keyword)) + 1))[: len(plaintext)]
    for x, y in zip(plaintext, keyword):
        if x.isupper():
            shift = ord(y.upper()) - ord("A")
            ciphertext += chr((ord(x) - ord("A") + shift) % 26 + ord("A"))
        elif x.islower():
            shift = ord(y.lower()) - ord("a")
            ciphertext += chr((ord(x) - ord("a") + shift) % 26 + ord("a"))
        else:
            ciphertext += x
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    keyword = (keyword * ((len(ciphertext) // len(keyword)) + 1))[: len(ciphertext)]
    for i, j in zip(ciphertext, keyword):
        if i.isupper():
            shift = ord(j.upper()) - ord("A")
            plaintext += chr((ord(i) - ord("A") - shift) % 26 + ord("A"))
        elif i.islower():
            shift = ord(j.lower()) - ord("a")
            plaintext += chr((ord(i) - ord("a") - shift) % 26 + ord("a"))
        else:
            plaintext += i
    return plaintext
