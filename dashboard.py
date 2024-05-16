import streamlit as st
# Import streamlit library
from st_on_hover_tabs import on_hover_tabs
# Import third party side hover tab module
from streamlit_local_storage import LocalStorage
# Import third party local storage module
from Classes.Bank import Bank
# Import Bank Class
import re
# Import regular expression
import pandas as pd
# Import Pandas for data manipulation

st.set_page_config(layout="wide")
# Setup page configuration streamlit

local_storage = LocalStorage()
# Create instance of local storage

st.header("Welcome to Trust Bank")
st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)
# Use style.css file for styles
st.markdown('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">', unsafe_allow_html=True)
# Use bootstrap cdn to use bootstrap modeules (navbar)
st.markdown('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" />', unsafe_allow_html=True)
# Use google icons cdn for side bar

st.markdown("""<nav class="navbar fixed-top navbar-expand-lg bg-body-tertiary" id="custom-navbar">
  <div class="container-fluid">
    <div class="container-fluid">
    <a class="navbar-brand" href="#">
      <span class="material-symbols-outlined">account_balance</span>
      Trust Bank
    </a>
  </div>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <form class="d-flex" role="search">
        <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
        <button class="btn btn-outline-dark" type="submit">Search</button>
      </form>
    </div>
  </div>
</nav>""", unsafe_allow_html=True)
# Top nav bar

if 'login_state' not in st.session_state:
  # Create login state in session state to keep the login status
  st.session_state.login_state = False


def show_tabs():
  # Side bar tabs
  if not st.session_state.login_state:
    with st.sidebar:#Side bar when not login
        tabs = on_hover_tabs(tabName = ['Dashboard',  'Register', 'Login'],
        iconName = ['dashboard', 'person_add', 'login'], 
        styles = { 'navtab': {'background-color':'#6b3497', 'color': '#ffffff', 'font-size': '18px', 'transition': '.3s', 'white-space': 'nowrap','text-transform': 'capitalize'},
                  'tabOptionsStyle': {':hover :hover': {'color': '#111', 'cursor': 'pointer'}},
                  'iconStyle':{'position':'fixed', 'left':'7px', 'text-align': 'left'}, 
                  'tabStyle' : {'list-style-type': 'none', 'margin-bottom': '30px', 'padding-left': '30px'}},
                    default_choice=0)
  else:
    with st.sidebar:#Side bar when login
        tabs = on_hover_tabs(tabName = ['Deposit', 'Withdraw', 'Check Balance', 'Transaction History', 'Logout'],
              iconName = ['credit_score','payments','account_balance_wallet', 'description', 'logout'], 
              styles = { 'navtab': {'background-color':'#6b3497', 'color': '#ffffff', 'font-size': '18px', 'transition': '.3s', 'white-space': 'nowrap','text-transform': 'capitalize'},
                'tabOptionsStyle': {':hover :hover': {'color': '#111', 'cursor': 'pointer'}},
                'iconStyle':{'position':'fixed', 'left':'7px', 'text-align': 'left'}, 
                'tabStyle' : {'list-style-type': 'none', 'margin-bottom': '30px', 'padding-left': '30px'}},
                default_choice=0)
  return tabs


bank = Bank()
# Create bank instance to handle account creation and other transaction activities
def create_account():
  # Get user inputs and create account
    st.subheader("Create new account")

    owner = st.text_input("Account holder name")
    if not owner.isalpha():# Validate input is alpha characters
      st.error("Please enter valid name", icon="🚨")

    initial_deposit = st.number_input("Initial deposit", min_value=0.0, step=0.1)

    acc_type = st.selectbox('Account Type', ['Savings Account','Current Account'])

    password_pattern = "^.*(?=.{6,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$"
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    valid_password = re.findall(password_pattern, password)#Validate password is matching with the pattern
    if not valid_password:
      st.error("Please enter valid password Password should be 6 characters, should contain uppercase A-Z, lowercase a-z, numbers 0-9, any special characters @#$%^&+=!", icon="🚨")

    if owner.isalpha() and initial_deposit and acc_type and password and confirm_password:
      #Check all input fields are filled and password and confirm password are matched after that view button to create account
      if not password == confirm_password:
        st.error("Confirm password deos not match!", icon="🚨")
      else:
        if st.button("Create Account"):
          account = bank.create_account(owner, initial_deposit, acc_type, password)
          # Create account instance throgh bank class instance
          st.session_state.acc_type = acc_type
          if account:
            st.success(f"{acc_type} created with number {account.get_account_number()}", icon='🎉')
    else:
      st.error("Please fill the details!", icon="🚨")
   
def deposit():
  # Deposit function to get input and command from user
  st.subheader("Deposit")
  deposit = st.number_input("Deposit amount", min_value=0.0, step=0.1)
  if st.button("Deposit"):
    bank.deposit(st.session_state.account_number, deposit)

def withdraw():
  # Withdraw function to get input and command from user
  st.subheader("Withdraw")
  withdraw = st.number_input("Withdraw amount", min_value=0.0, step=0.1)
  if st.button("Withdraw"):
    bank.withdraw(st.session_state.account_number, withdraw)

def check_balance():
  # Withdraw function to enable user to view the current balance
  st.subheader("Check Balance")
  balance = bank.check_balance(st.session_state.account_number)
  st.write("Your account balance is ",balance)
  bank.print_account(st.session_state.account_number)

def transaction_log():
  # Enable user to view the transaction history
  st.subheader("Transaction History")
  transaction = bank.display_transaction(st.session_state.account_number)
  data_frame_columns = ['Transaction', 'Amount', 'Date', 'Balance']
  data_frame = pd.DataFrame(transaction, columns=data_frame_columns)
  st.dataframe(data_frame, use_container_width=True)

def logout():
  # Logout the current session
  st.subheader("Logout")
  st.image('./images/transaction.png', width=400)
  if st.button("Logout"):
    st.session_state.login_state = False
    st.session_state.account_number = None
    show_tabs()
    local_storage.deleteItem(itemKey="login")
    st.experimental_rerun()
  st.success("Thank you for banking with Trust Bank, Welcome Again", icon="🎉")
  
def login():
    st.subheader("Login")
    account_number = st.text_input("Account Number", placeholder="Account number")
    password = st.text_input("Enter Password", placeholder="Password")
    if st.button("Login"):
        account = bank.get_account(account_number, password)
        if account:
          st.success('You successfully logged in!', icon="✅")
          local_storage.setItem(itemKey = "login", itemValue = True, key= "login_key")
          st.session_state.login_state = True
          if 'account_number' not in st.session_state:
            st.session_state.account_number = bank.exist_account_number(account_number)
          show_tabs()
        else:
          if not bank.exist_account_number(account_number):
            st.error("Account number does not exist!", icon="🚨")
          else:
            if not password == bank.get_acc_password(account_number):
              st.error("Invalid Password", icon="🚨")
            else:
              st.error("An unexpected error occurred. Please try again", icon="🚨")

if __name__ == "__main__":
#Display particular contents according to selected tabs
  tabs = show_tabs()
  if tabs == 'Dashboard':
    st.title("Dashboard")
    st.write("Don't have an account?")
    st.markdown('<p><span class="material-symbols-outlined" style="vertical-align: middle;">arrow_back</span> Hover here to register</p>', unsafe_allow_html=True)
    st.image('./images/bank.png', width=400)
  elif tabs == 'Register':
    create_account()
  elif tabs == 'Login':
    login()
  elif tabs == 'Deposit':
    deposit()
  elif tabs == 'Withdraw':
    withdraw()
  elif tabs == 'Check Balance':
    check_balance()
  elif tabs == 'Transaction History':
    transaction_log()
  elif tabs == 'Logout':
    logout()
