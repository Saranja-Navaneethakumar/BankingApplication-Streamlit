from .Account import Account
from .SavingAccount import SavingAccount
from .CurrentAccount import CurrentAccount
import random
# To generate bank account number

class Bank:

    _accounts = [] #List to store created accounts

    def create_account(self, name, initial_deposit, acc_type, password):
        #Function for create new account and return account
        account_number = self.generate_account_number()
        if(acc_type == 'Savings Account'):
            account = SavingAccount(name, account_number, initial_deposit, 'Savings Account' ,password)
        elif(acc_type == 'Current Account'):
            account = CurrentAccount(name, account_number, initial_deposit, 'Current Account' ,password)
        else:
            account = Account(name, account_number, initial_deposit, password)
        self._accounts.append(account)
        return account


    def generate_account_number(self):
        # Generate random 6 digit number for user account number
        return f"{random.randint(100000, 999999)}"

    def get_account(self, account_number, password):
        #Get account by its account number and password
        for account in self._accounts:
            if account.get_account_number() == account_number and account.get_password() == password:
                return account
            else:
                return None

    def exist_account_number(self, account_number):
        #Check whether an account with the given account number exist
        for account in self._accounts:
            if account.get_account_number() == account_number:
                return account.get_account_number()
            else:
                return False

    def get_acc_password(self, account_number):
        #Get password of the account for the given account number
        for account in self._accounts:
            if account.get_account_number() == account_number:
                return account.get_password()
            else:
                return False

    def deposit(self, acc_no, amount):
        #Deposit amount into the account for the given account number
        for account in self._accounts:
            if account.get_account_number() == acc_no:
                account._deposit(amount)
            
    def withdraw(self, acc_no, amount):
        #Withdraw amount into the account for the given account number
        for account in self._accounts:
            if account.get_account_number() == acc_no:
                account._withdraw(amount)

    def check_balance(self, acc_no):
        #Check the balance of the account for the given account number
        for account in self._accounts:
            if account.get_account_number() == acc_no:
                return account.display_balance()

    def print_account(self, acc_no):
        #Print the details for the account for the given account number
        for account in self._accounts:
            if account.get_account_number() == acc_no:
                account.display_account()

    def display_transaction(self, acc_no):
        #Display transaction history for the account for the given account number
        for account in self._accounts:
            if account.get_account_number() == acc_no:
                return account.display_transaction_log()