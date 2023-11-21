def caesar_encode(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            if char.islower():
                result += chr(((ord(char) - 97 + shift) % 26) + 97)
            else:
                result += chr(((ord(char) - 65 + shift) % 26) + 65)
        else:
            result += char
    return result

def caesar_decode(text, shift):
    return caesar_encode(text, -shift)