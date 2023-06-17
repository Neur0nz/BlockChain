from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import Crypto.Random
import binascii
class Wallet:
    """
    the wallet lol
    """

    def __init__(self, node_id):
        self.private_key = None
        self.public_key = None
        self.node_id = node_id


    def create_keys(self):
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key
    
    def save_keys(self):
        if self.public_key != None and self.private_key != None:
            try:
                with open(f'wallet-{self.node_id}.txt', 'w') as f:
                    f.write(f'{self.private_key}\n{self.public_key}')
                return True
            except (IOError, IndexError):
                #print saving failed in bright red color (\033[91m)
                print('\033[91mSaving New Private Key and Public Key to file failed.\033[0m')
                return False
        else:
            print('\033[91mNo Private Key or Public Key to save.\033[0m')
            return False

    def load_keys(self):
        try:
            with open(f'wallet-{self.node_id}.txt','r') as f:
                keys = f.readlines()
                self.private_key = keys[0][:-1]
                print(self.private_key)
                self.public_key = keys[1][:]
            return True
        except (IOError, IndexError):
            print('\033[91mLoading Private Key and Public Key from file failed.\033[0m')
            return False


    def generate_keys(self):
        private_key = RSA.generate(1024, Crypto.Random.new().read)
        public_key = private_key.publickey()
        return (binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'), binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii'))

    def sign_transaction(self, sender, recipient, amount):
        signer = PKCS1_v1_5.new(RSA.importKey(binascii.unhexlify(self.private_key)))
        h = SHA256.new((str(sender) + str(recipient) + str(amount)).encode('utf8'))
        signature = signer.sign(h)
        return binascii.hexlify(signature).decode('ascii')
    @staticmethod
    def verify_transaction_signature(transaction):
        public_key = RSA.importKey(binascii.unhexlify(transaction.sender))
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA256.new((str(transaction.sender) + str(transaction.recipient) + str(transaction.amount)).encode('utf8'))
        return verifier.verify(h, binascii.unhexlify(transaction.signature))
