from datetime import datetime
import hashlib

class Block:
    def __init__(self, index, previous_hash, transactions, proof, timestamp=None):
        """
        Represents a block in the blockchain.

        Args:
            index (int): The index of the block.
            previous_hash (str): The hash of the previous block in the blockchain.
            transactions (list): List of transactions included in the block.
            proof (int): The proof of work number.
            timestamp (float, optional): The timestamp of the block creation. If not provided, the current timestamp will be used.
        """
        self.index = index
        self.timestamp = datetime.now().timestamp() if timestamp is None else timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.proof = proof

    def __repr__(self):
        """
        Returns a string representation of the block.

        Returns:
            str: The string representation of the block.
        """
        return f'Block: Index: {self.index} | Timestamp: {self.timestamp} | Transactions: {self.transactions} | Previous Hash: {self.previous_hash} | Proof: {self.proof}'