# made by Darien Fodor and Alex Runholt
# Used https://stegano.readthedocs.io/en/latest/module.html
# see readme.txt for manual

Bfrom datetime import datetime
from stegano import lsb
#from Crypto.Cipher import AES
import secrets
import argparse


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

encrypt.add_argument('--iv', type=str, help='if not included a 16 byte initial value(nonce) will be generated')
encrypt.add_argument('-k', '--key', type=str, help='if not included a 32 byte key will be generated')

# decryption arguments
dec_group = decrypt.add_mutually_exclusive_group()
dec_group.add_argument('-d', '--decrypt', action='store_true', help='perform decryption on text inside image')
dec_group.add_argument('-x', '--extract', action='store_true', help='extract raw text from inside image')

decrypt.add_argument('--iv', type=str, help='Enter IV')
decrypt.add_argument('-k,', '--key', type=str, help='Enter Key')
decrypt.add_argument('-m', '--image', type=str, help='Image which serves as a package')

# parse args
args = parser.parse_args()


def generate_key():
    new_key = secrets.token_bytes(32)
    return new_key
def generate_iv():
    new_iv = secrets.token_bytes(16)
    return new_iv
# creating encryption
def AES_encrypt(plain_text, enc_iv, enc_key):
    obj = AES.new(enc_key, AES.MODE_CFB, enc_iv)
    enc_text = obj.encrypt(plain_text)
    return enc_text
# creating decryption
def AES_decrypt(enc_text, dec_iv, dec_key):
    obj = AES.new(dec_key, AES.MODE_CFB, dec_iv)
    plain_text = obj.decrypt(enc_text)
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
            cleartext = file.read()
    if args.insert:
        new_image = image_encrypt(cleartext, args.image)
        print("new image: ", new_image)

    elif args.encrypt:
        # generate key
        if args.key:
            key = args.key
        else:
            key = generate_key()
        # generate iv
        if args.iv:
            iv = args.iv
        else:
            iv = generate_iv()

        new_ciphertext = AES_encrypt(cleartext, iv, key)
        secret = image_encrypt(new_ciphertext, args.image)
        print("key:", key)
        print("IV:", iv)
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
