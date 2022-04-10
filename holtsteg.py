# made by Darien Fodor and Alex Runholt
# Used https://stegano.readthedocs.io/en/latest/module.html
# see readme.txt for manual

import argparse
from datetime import datetime
from stegano import lsb
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode

parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest='command')
encrypt = subparser.add_parser('encrypt')
decrypt = subparser.add_parser('decrypt')

# encryption arguments
ins_group = encrypt.add_mutually_exclusive_group()
ins_group.add_argument('-i', '--insert', action='store_true', help='Do not encrypt the plaintext inside the package, just insert it')
ins_group.add_argument('-c', '--encrypt', action='store_true', help='Encrypt the plaintext')

enc_group = encrypt.add_mutually_exclusive_group()
enc_group.add_argument('-p', '--plaintext', type=str, help='plaintext input is typed into terminal')
enc_group.add_argument('-f', '--file', type=str, help='input is a file')

# encrypt.add_argument('plain_input', type=str, help='message to be encrypted, if not in a file surround with quotes')
encrypt.add_argument('-m', '--image', type=str, help='image which serves as a package')


# decryption arguments
dec_group = decrypt.add_mutually_exclusive_group()
dec_group.add_argument('-d', '--decrypt', action='store_true', help='perform decryption on text inside image')
dec_group.add_argument('-x', '--extract', action='store_true', help='extract raw text from inside image')

decrypt.add_argument('--iv', type=str, help='Enter IV')
decrypt.add_argument('-k,', '--key', type=str, help='Enter Key')
decrypt.add_argument('-m', '--image', type=str, help='Image which serves as a package')

# parse args
args = parser.parse_args()


# creating encryption
def AES_encrypt(plaintext):
    new_key = get_random_bytes(32)
    plaintext_raw = plaintext.encode("utf8")
    cipher = AES.new(new_key, AES.MODE_CFB)
    ciphertext_raw = cipher.encrypt(plaintext_raw)
    iv = b64encode(cipher.iv).decode('utf-8')
    ciphertext = b64encode(ciphertext_raw).decode('utf-8')
    readable_key = b64encode(new_key).decode('utf-8')
    return ciphertext, iv, readable_key
# creating decryption
def AES_decrypt(ciphertext, dec_iv, dec_key):
    raw_iv = b64decode(dec_iv)
    raw_key = b64decode(dec_key)
    raw_ciphertext = b64decode(ciphertext)
    cipher = AES.new(raw_key, AES.MODE_CFB, iv=raw_iv)
    plain_text = cipher.decrypt(raw_ciphertext)
    return plain_text
# lsb encryption in image
def image_encrypt(ciphertext, image):
    secretImage = lsb.hide(image, ciphertext)
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d_%H%M%S")
    secret_image = ("secret" + dt_string + ".png")
    secretImage.save(secret_image)
    return secretImage
# lsb image
def image_extract(image):
    extracted_ciphertext = lsb.reveal(image)
    return extracted_ciphertext


# main encryption
if args.command == "encrypt":
    # is the plaintext input a file or an argument
    if args.plaintext:
        cleartext = args.plaintext
    elif args.file:
        with open(args.file) as file:
            filetext = file.read()
            cleartext = filetext
    if args.insert:
        new_image = image_encrypt(cleartext, args.image)
        print("new image: ", new_image)

    elif args.encrypt:
        # generate key

        new_ciphertext, IV, formatted_key = AES_encrypt(cleartext)

        secret = image_encrypt(new_ciphertext, args.image)
        print("IV:", IV)
        print("Key:", formatted_key)
        print("Secret image:", secret)

# main decryption
elif args.command == "decrypt":
    print('decryption', args.command)
    hidden_text = image_extract(args.image)
    if args.decrypt:
        plaintext = AES_decrypt(hidden_text, args.iv, args.key)
        print("text decrypted:", plaintext)
    if args.extract:
        print('text extracted:', image_extract(args.image))

else:
    print("please put a valid option, type -h to see options")
