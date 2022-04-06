# holtsteg
# Python Encryption and Steganography tool
# made by Darien Fodor and Alex Runholt
# depentdant on stegano and pyCryptodrome

usage: holtsteg.py [-h] {encrypt,decrypt} ...

positional arguments:
  {encrypt,decrypt}
options:
  -h, --help            show this help message and exit


usage: holtsteg.py encrypt [-h] [-i | -c] [-p PLAINTEXT | -f FILE] [-m IMAGE] [--iv IV]
                           [-k KEY]

options:
  -h, --help            show this help message and exit
  -i, --insert          Do not encrypt the plaintext inside the package, just insert it    
  -c, --encrypt         Encrypt the plaintext
  -p PLAINTEXT, --plaintext PLAINTEXT
                        plaintext input is typed into terminal
  -f FILE, --file FILE  input is a file
  -m IMAGE, --image IMAGE
                        image which serves as a package
  --iv IV               if not included a 16 byte initial value(nonce) will be generated
  -k KEY, --key KEY     if not included a 32 byte key will be generated

usage: holtsteg.py decrypt [-h] [-d | -x] [--iv IV] [-k, KEY] [-m IMAGE]

options:
  -h, --help            show this help message and exit
  -d, --decrypt         perform decryption on text inside image
  -x, --extract         extract raw text from inside image
  --iv IV               Enter IV
  -k, KEY, --key KEY    Enter Key
  -m IMAGE, --image IMAGE
                        Image which serves as a package
