from collections import OrderedDict

class Transaction:
    def __init__(self, sender, recipient, signature, amount):
        """
        Represents a transaction in the blockchain.

        Args:
            sender (str): The sender of the transaction.
            recipient (str): The recipient of the transaction.
            signature (str): The signature of the transaction.
            amount (float): The amount of the transaction.
        """
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature

    def get_amount(self):
        """
        Get the amount of the transaction.

        Returns:
            float: The amount of the transaction.
        """
        return self.amount

    def __repr__(self):
        """
        Returns a string representation of the transaction.

        Returns:
            str: The string representation of the transaction.
        """
        return f'Transaction: Sender: {self.sender} | Recipient: {self.recipient} | Amount: {self.amount}'

    def to_ordered_dict(self):
        """
        Converts the transaction to an ordered dictionary.

        Returns:
            OrderedDict: The transaction as an ordered dictionary.
        """
        return OrderedDict([('sender', self.sender), ('recipient', self.recipient), ('amount', self.amount)])