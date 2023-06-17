from inspect import signature
from uuid import uuid4
from blockchain import Blockchain
from utility.verification import Verification
from wallet import Wallet
class Node:


    def __init__(self):
        self.wallet = Wallet()
        self.blockchain = None
        
    

    def listen_for_input(self):
        running =True
        while running:
            print("-------------------")
            print()
            choice = self.get_choice()
            #choice is the users action he wants to do this iteration
            if choice =='1':
                if self.take_transaction():
                    print("\033[92m transaction added sucessfully \033[0m")
                else:
                    print("\033[93m\033[1minvalid transaction ,try again. \033[0m")
            elif choice =='2':
                self.print_blockchain()
            elif choice=='q':
                running = False
            elif choice =='3':
                if not self.blockchain.mine_block():
                    print("\033[93m\033[1mMining failed. \033[0m")
            elif choice =='4':
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif choice =='7':
                self.wallet.save_keys()
            elif choice =='5':
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print("All transactions are valid")
                else:
                    print("There are invalid transactions")
            elif choice =='6':
                try:
                    self.wallet.load_keys()
                    self.blockchain = Blockchain(self.wallet.public_key)
                    print("\033[92m Wallet loaded sucessfully \033[0m")
                except:
                    print("\033[93m\033[1mWallet load failed \033[0m")
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print("\033[92m All transaction are valid. \033[0m")
                else:
                    print("there are invalid transactions")
            if Verification.chain_verifier(blockchain=self.blockchain.get_chain()):
                print('\033[2;31;43m The Blockchain has been compromised , shutting down \033[0;0m')
                running = False
                break
            print("balance of {} is: {:6.2f}".format(self.wallet.public_key,self.blockchain.get_balance()))
        else:
            print("loop stopped running")


    def get_choice(self):
        print("1:make a transaction.")
        print("2:print current blockchain.")
        print("3:mine a new block.")
        print("4:create a new wallet")
        print("5:check transaction validity")
        print("6:load wallet from file")
        print("7:save wallet to file")
        print("q:quit software.")
        return input("input: ")


    def print_blockchain(self):
        print(self.blockchain.chain)


    def get_transaction_info(self):
        """ Returns the input of the user (a new transaction amount) as a float. """
        in_recipient = input('Enter name of recipient: ')
        in_amount = float(input('Your transaction amount please: '))
        return in_recipient, in_amount


    def take_transaction(self):
        """ takes in transaction data and adds it to the blockchain. """
        tx_data = self.get_transaction_info()
        recipient, amount = tx_data
        signature = self.wallet.sign_transaction(self.wallet.public_key, recipient, amount)
        return self.blockchain.add_transaction(recipient=recipient, sender=self.wallet.public_key, signature=signature, amount=amount)
if __name__ == '__main__':
    node = Node()
    node.listen_for_input()