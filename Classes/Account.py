from datetime import datetime
import streamlit as st

class Account:

    __acc_holder_name = None # Name of the account holder
    __account_number = None # Account number
    __acc_balance = 0 # Account balance
    __acc_transaction = None # List to store the account transactions
    __created_time = None # Timestamp when accout, transactions created
    _error_message = None # Error message for fail scenarios
    _success_message = None # Success message for successful scenarios
    __basic_amount = 10 # Minimum amount to maintain the account
    __password = None # password of the account
    
    def __init__(self, name, account_number, balance, password):
        #Constructor to initialize an account object
        self.__acc_holder_name = name
        self.__account_number = account_number
        self.__acc_balance = balance
        self.__acc_transaction = []
        self.__password = password
        self.__created_time = datetime.now()
        self.__acc_transaction.append(('Account created', balance, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.__acc_balance))


    def _deposit(self, amount, interest=False):
        #Depsoit ammount to the account, update balance, transaction history and provide messages
        if(amount > 0):
            self.__acc_balance += amount
            if interest:
                # Check the deposit is interest and execte the repective functions
                self.__acc_transaction.append(('Interest', amount, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.__acc_balance))
                self._success_message = f"Your interest is {amount}, Your balance is {self.__acc_balance}"
            else:
                self.__acc_transaction.append(('Deposit', amount, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.__acc_balance))
                self._success_message = f"You successfully deposited {amount}, Your balance is {self.__acc_balance}"
            st.success(self._success_message, icon="✅")
        else:
            self._error_message = "Invalid Amount"
            st.error(self._error_message, icon="🚨")

    def _withdraw(self, amount):
        #Withdraw amount from the account, update balance, transaction history and provide messages
        if(amount > 0):
            if(self.__acc_balance-(amount+self.__basic_amount) >= 0):
                self.__acc_balance -= amount
                self.__acc_transaction.append(('Withdraw', amount, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.__acc_balance))
                self._success_message = f"You successfully withdrawed {amount}, Your balance is {self.__acc_balance}"
                st.success(self._success_message, icon="✅")
            else:
                self._error_message = f"Insufficient balance!, You can only withdraw {self.__acc_balance-self.__basic_amount}"
                st.error(self._error_message, icon="🚨")
        else:
            self._error_message = "Invalid Amount"
            st.error(self._error_message, icon="🚨")


    def display_balance(self):
        #Display the current balance of the account
        return self.__acc_balance

    def display_transaction_log(self):
        #Display transaction history of the account
        return self.__acc_transaction

    def get_account_number(self):
        #Retrieve the account number
        return self.__account_number

    def get_password(self):
        #Retrieve the password associated to the account
        return self.__password

    def display_account(self):
        print("acc no", self.__account_number, "balance", self.__acc_balance, "holder name", self.__acc_holder_name, "passwor", self.__password)

    def add_interest(self, rate):
        #Add interest to the current account balance
        #This function will further implemet in the subclasses according to their account types and diffrent interest rates
        pass
