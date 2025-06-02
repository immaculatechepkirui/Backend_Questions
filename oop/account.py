from datetime import datetime



class Transaction:
    def __init__(self, narration, amount, transaction_type):
        self.date_time = datetime.now().strftime("%Y-%m-%d%H:%M:%S")
        self.narration = narration
        self.amount = amount
        self.transaction_type = transaction_type

    def __str__(self):
        return f"{self.date_time} | {self.transaction_type} | {self.amount} | {self.narration}"



class Account():
    def __init__(self, owner,initial_balance=0, min_balance=0):
        self.owner = owner
        self._balance = initial_balance
        self.min_balance = min_balance
        self.transactions = []
        self._loan_balance = 0
        self.frozen = False

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            transaction = Transaction("Deposit", amount, "Credit")
            self.transactions.append(transaction)
            return f"Confirmed. Deposit successful. Your new balance is {self._balance}"
        return "Deposit amount must be positive"
    

    def withdraw(self, amount):
        if self.frozen:
            return "Your account is frozen. Cannot withdraw."
        if amount > 0 and self._balance - amount >= self.min_balance:
            self._balance -= amount
            transaction = Transaction("Withdrawal", amount, "Debit")
            self.transactions.append(transaction)
            return f"Confirmed. Withdrawal successful.Your new balance is {self._balance}"
        return "Insufficient balance to withdraw"
    
    def transfer_funds(self, amount, recipient_account):
        if self.frozen:
            return "Account is frozen. Cannot transfer funds."
        if amount > 0 and self._balance - amount >= self.min_balance:
            self._balance -= amount
            recipient_account += amount
            sender_transaction = Transaction(f"Transferred to {recipient_account.owner}", amount, "Debit")
            recipient_transaction = Transaction(f"Received from {self.owner}", amount, "Credit")
            self.transactions.append(sender_transaction)
            recipient_account(recipient_transaction)
            return f"Transfer successful. New balance: {self._balance}"
        return "Insufficient funds or below minimum balance."

    

    def get_balance(self):
        return f"Your current balance is {self.balance}"
    

    def request_loan(self, amount):
        if self.frozen:
            return "Loan request denied. Account is frozen."
        if amount <= 0:
            return "Loan amount must be positive."
        if len(self.transactions) < 3:
            return "Loan request denied. Account must have at least 3 transaction records."
        if self._balance < 100:
            return "Loan request denied. Maintain a minimum balance before applying."
        if amount > self._balance * 0.5:
            return "Loan request denied. You can only borrow up to 50% of your balance."
        

        self._loan_balance += amount
        self._balance += amount
        transaction = Transaction("Loan Approved", amount, "Credit")
        self.transactions.append(transaction)
        return f"Loan of {amount} approved."

    

    def repay_loan(self, amount):
        if amount > 0 and amount <= self._loan_balance:
            self._loan_balance -= amount
            self._balance -= amount
            transaction = Transaction("Loan Repayment", amount, "Debit")
            self.transactions.append(transaction)
            return f"Loan repayment successful. Remaining loan balance: {self._loan_balance}"
        return "Invalid repayment amount."

        
    

    def view_account_details(self):
        return f"Account Owner: {self.owner}\nAccount Number: {self._account_number}\nBalance: {self._balance}\nLoan Balance: {self._loan_balance}"

    

    def change_account_owner(self, new_owner):
        self.owner = new_owner
        return f"Account owner has successfully been changed to {new_owner}"
    

    def account_statement(self):
        return "\n".join(str(transaction) for transaction in self.transactions)

    

    def interest_calculation(self):
        interest = self._balance * 0.05
        self._balance += interest
        transaction = Transaction("Interest Added", interest, "Credit")
        self.transactions.append(transaction)
        return f"Interest applied. New balance: {self._balance}"

    
    def freeze_account(self):
        self.frozen = True
        transaction = Transaction("Account Frozen", 0, "Info")
        self.transactions.append(transaction)
        return "Account has been frozen."

    

    def unfreeze_account(self):
        self.frozen = False
        transaction = Transaction("Account Unfrozen", 0, "Info")
        self.transactions.append(transaction)
        return "Account has been unfrozen."

    

    def set_minimum_balance(self, amount):
        if amount >= 0:
            self.min_balance = amount
            return f"Minimum balance set to {amount}"
        return "Minimum balance must be non-negative."


    def close_account(self):
        self.balance = 0
        self.loan_balance = 0
        self.transactions = []
        return "Your account has been successfully closed"
    

    def close_account(self):
        transaction = Transaction("Account Closed", self._balance, "Info")
        self.transactions.append(transaction)
        self._balance = 0
        self._loan_balance = 0
        self.transactions = []
        return "Account closed. All balances reset."

    