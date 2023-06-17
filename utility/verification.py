"""verification stuff"""
from utility.hashing_util import hash_block, hash_string_256
from transaction import Transaction
from block import Block
from wallet import Wallet
class Verification:
    @classmethod
    def chain_verifier(cls, blockchain):
        '''checks if the block chain has been tempered and return True if its has and False if its not been'''
        for (i,block) in enumerate(blockchain):
            if i==0: continue
            if block.previous_hash !=hash_block(blockchain[i-1]):
                return True
            if not cls.valid_proof(block.transactions[:-1],block.previous_hash,block.proof):
                print("Proof of work is invalid")
                return True
        return False 

    @staticmethod
    def verify_transaction(transaction,get_balance,check_funds=True):
        '''verifies the transaction and returns True if its valid and False if its not'''
        if check_funds:
            sender_balance = get_balance(transaction.sender)
            return sender_balance >= transaction.amount and Wallet.verify_transaction_signature(transaction)
        return Wallet.verify_transaction_signature(transaction)

    @classmethod
    def verify_transactions(cls, open_transactions, get_balance):
        return all([cls.verify_transaction(tx, get_balance) for tx in open_transactions])
    
    @staticmethod
    def valid_proof(transactions, last_hash, proof, difficulty=5):
        guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(last_hash) + str(proof)).encode()
        guess_hash = hash_string_256(guess)
        return guess_hash[0:difficulty] == '0' * difficulty

