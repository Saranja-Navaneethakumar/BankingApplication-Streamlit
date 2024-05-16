from .Account import Account
import streamlit as st

class SavingAccount(Account):
    _interest_rate = 0.01
    acc_type = None

    def __init__(self, name, account_number, balance, acc_type, password):
        #Call the parent class's constructor (Account)
        super().__init__(name, account_number, balance, password)
        #Calculate interest and add to the balance through deposit
        interest = self.add_interest(balance)
        super()._deposit(interest, interest=True)
        #Display success messsage for interest rate
        self._success_message = f"You have {self._interest_rate*100}% interest rate!"
        st.success(self._success_message, icon="✅")
        #Set account type
        self.acc_type = acc_type

    def add_interest(self, amount):
        #Calculate the interest based on the deposit amount
        if amount>0:
            amount = amount*self._interest_rate
        return amount
