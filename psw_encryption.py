import string
chars = list(string.printable+string.printable+string.printable+string.printable+string.printable)
key = '45179898572957296'

def encrypt(psw):

    index_len_psw_in_key = key[len(psw)]

    encrypted_psw = r''
    count = 0
    for i in psw:

        index_in_chars = chars.index(i)
        
        encrypted_char = chars[index_in_chars + (int(index_len_psw_in_key)*int(key[count]))]
        count += 1
        encrypted_psw += encrypted_char
    
    return encrypted_psw


def decrypt(psw):
    index_len_psw_in_key = key[len(psw)]

    decrypted_psw = r''
    count = 0
    for i in psw:
        index_in_chars = chars.index(i)
        decrypted_char = chars[index_in_chars-(int(index_len_psw_in_key)*int(key[count]))]
        count += 1
        decrypted_psw += decrypted_char

    return decrypted_psw

