"""
This module is used to create a blockchain and manage transactions
"""
import json
import functools
import requests
from utility.verification import Verification
from utility.hashing_util import hash_block
from block import Block
from transaction import Transaction
from wallet import Wallet

MINING_REWARD = 10


class Blockchain:
    """
    the following methods are used to create a new blockchain
    """
    def __init__(self, public_key, node_id):
        GENESIS_BLOCK = Block(0, '', [], 69,timestamp=0)
        self.chain = [GENESIS_BLOCK]
        self.__open_transactions = []
        self.public_key = public_key
        self.node_id = node_id
        self.resolve_conflicts = False
        print(f'the node id is: {node_id}')
        self.__peer_nodes = set()
        self.load_data()


    @property
    def chain(self):
        """ Returns the chain property. """
        return self.__chain[:]
    @chain.setter
    def chain(self, val):
        self.__chain = val


    def save_data(self):
        """ Save blockchain + open transactions to a file """
        try:
            with open(f'blockchain-{self.node_id}.txt', mode='w') as f:
                saveable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in self.__chain]]
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                saveable_tx = [tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(saveable_tx))
                f.write('\n')
                f.write(json.dumps(list(self.__peer_nodes)))
                # save_data = {'chain': blockchain, 'ot': open_transactions}
                # f.write(pickle.dumps(save_data))
        except IOError:
            print('Saving failed!')


    def load_data(self):
        try:
            with open(f'blockchain-{self.node_id}.txt', mode='r') as f:
                # file_content = pickle.loads(f.read())
                file_content = f.readlines()
                # blockchain = file_content['chain']
                # open_transactions = file_content['ot']
                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(tx['sender'], tx['recipient'],tx['signature'], tx['amount']) for tx in block['transactions']]
                    updated_block = Block(
                        block['index'], block['previous_hash'], converted_tx, block['proof'],block['timestamp'])
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain
                open_transactions = json.loads(file_content[1][:-1])
                updated_transactions = []
                for tx in open_transactions:
                    updated_transaction = Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount'])
                    updated_transactions.append(updated_transaction)
                self.__open_transactions = updated_transactions
                self.__peer_nodes = json.loads(file_content[2])
        except (IOError, IndexError):
            print('Loading failed!')
        finally:
            print('done loading data')


    def get_last_blockchain_value(self):
        """ Returns the last value of the current blockchain. """
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]

    def add_transaction(self, recipient,sender, signature, amount, is_recieving=False):
        """ Append a new value as well as the last blockchain value to the blockchain.
        
        Arguments:
            :snder: sender of coins.
            :recipient: reciever of coins.
            :amount: transaction amount.
        """
        # if self.public_key == None:
        #     return False
        transaction = Transaction(sender, recipient, signature, amount)
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            if not is_recieving:
                for node in self.__peer_nodes:
                    url = f'http://{node}/broadcast-transaction'
                    try:
                        response = requests.post(url, json={'sender': sender, 'recipient': recipient, 'amount': amount, 'signature': signature})
                        if response.status_code == 400 or response.status_code == 500:
                            print('Transaction declined, needs resolving')
                            return False
                    except requests.exceptions.ConnectionError:
                        continue
            return True
        return False
    def resolve(self):
        """Checks all peer nodes to see if any of them has a longer chain than ours."""
        for node in self.__peer_nodes:
            url = f'http://{node}/chain'
            replaced = False
            try:
                response = requests.get(url)
                node_chain = response.json()
                node_chain = [Block(block['index'], block['previous_hash'], [Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']], block['proof'], block['timestamp']) for block in node_chain]
                node_chain_length = len(node_chain)
                local_chain_length = len(self.__chain)
                if node_chain_length > local_chain_length and Verification.chain_verifier(node_chain):
                    self.__chain = node_chain
                    replaced = True
            except requests.exceptions.ConnectionError:
                print(f"Node: '{node}' is unreachable")
        self.resolve_conflicts = False
        if replaced:
            self.__open_transactions = []
        self.save_data()
        return replaced

    def get_chain(self):
        """ Returns the blockchain. """
        return self.__chain[:]


    def get_open_transactions(self):
        return self.__open_transactions[:]

    def mine_block(self):
        """ mine the current unverified transactions and add them to the blockchain"""
        if self.public_key == None:
            return None
        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        reward_transaction = Transaction('MINING', self.public_key, '', MINING_REWARD)
        copied_transactions = self.__open_transactions[:]
        for tx in copied_transactions:
            if not Wallet.verify_transaction_signature(tx):
                return None
        copied_transactions.append(reward_transaction)
        self.__open_transactions.append(reward_transaction)
        block = Block(len(self.__chain), hashed_block, copied_transactions, proof)
        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()
        for node in self.__peer_nodes:
            url = f'http://{node}/broadcast-block'
            print(f'broadcasting block to {node}')
            converted_block = block.__dict__.copy()
            converted_block['transactions'] = [tx.__dict__ for tx in converted_block['transactions']]
            try:
                response = requests.post(url, json={'block': converted_block})
                if response.status_code == 400 or response.status_code == 500:
                    print('Block declined, needs resolving')
                if response.status_code == 409:
                    self.resolve_conflicts = True
            except requests.exceptions.ConnectionError:
                print('Error: unable to reach server')
        return block


    def get_balance(self, sender=None):
        """ Returns the balance of the node. """
        if sender == None:
            if self.public_key == None:
                return None
            participant = self.public_key
        else:
            participant = sender
        tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in self.__chain]
        open_tx_sender = [tx.amount for tx in self.__open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
        tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in self.__chain]
        amount_received = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
        return amount_received - amount_sent

    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1
        return proof
    
    def add_peer_node(self, node):
        """ Add a new node to the peer node set. 
            the node is a url/ ip probably. """
        self.__peer_nodes.add(node)
        self.save_data()
    
    def remove_peer_node(self, node):
        """ Remove a node from the peer node set."""
        self.__peer_nodes.discard(node)
        self.save_data()
    
    def get_peer_nodes(self):
        """returns all peer nodes as a list."""
        return list(self.__peer_nodes)
    
    
    def add_block(self, block):
        transactions = [Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']]
        proof_is_valid = Verification.valid_proof(transactions[:-1], block['previous_hash'], block['proof'])
        hashes_match = hash_block(self.chain[-1]) == block['previous_hash']
        if not proof_is_valid or not hashes_match:
            return False
        converted_block = Block(block['index'], block['previous_hash'], transactions, block['proof'], block['timestamp'])
        self.__chain.append(converted_block)
        stored_transactions = self.__open_transactions[:]
        for itx in block['transactions']:
            for opentx in stored_transactions:
                if opentx.sender == itx['sender'] and opentx.recipient == itx['recipient'] and opentx.amount == itx['amount'] and opentx.signature == itx['signature']:
                    try:
                        self.__open_transactions.remove(opentx)
                    except ValueError:
                        print('Item was already removed')
        self.save_data()