# <------------------------ Imports ------------------------------> #

from __init__ import conn, start_connection
from funcs import *
import sys
if sys.version >= "3.0.0": #PySimpleGUI
    import PySimpleGUI as sg
    from PySimpleGUI import Window, T, Input, Button, Popup, PopupError, Submit, TabGroup, Tab
else:
    import PySimpleGUI27 as sg
    from PySimpleGUI27 import Window, T, Input, Button, Popup, PopupError, Submit, TabGroup, Tab

import datetime
import matplotlib.pyplot as plt
import csv
from typing import *
# <------------------------- Useful Stuff ---------------------------------> #

tooltips = [
    'Log a new transaction',
    'Quickly jot down transactions and make calculations. Export them to a csv file',
    'View graphs of your expenditure and income history',
    'See all of your transactions'
]

heading_format = {
    "justification": 'center',
    "size":  (10, 1),
    "font":  "Segoe"
}

year = datetime.datetime.now().year
month = datetime.datetime.now().month
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# <----------------------- MySQL -----------------------------> #

'''
  __  __       ____   ___  _
 |  \/  |_   _/ ___| / _ \| |
 | |\/| | | | \___ \| | | | |
 | |  | | |_| |___) | |_| | |___
 |_|  |_|\__, |____/ \__\_\_____|
         |___/

Here below lie all the MySQL related functions. Queries, connectivity (actually in __init__.py), cursors, 
everything's here.
'''

start_connection()  # Starts MySQL Database


def check_login_info(User: str, Pass: str) -> bool:
    cursor = conn.cursor()

    try:
        cursor.execute(f"""
        SELECT username, passwd
        FROM users 
        WHERE username = '{User}' AND passwd = '{Pass}';
        """)

        result = cursor.fetchone()
        if result not in [[], None, [()]]:
            return True

        else:
             return False

    except ConnectionError:
        Popup("Error Connecting to Database.",
              "Please try again or restart the program")

    cursor.close()


def create_account(u: Union[str, int], p: Union[str, int], e: Union[str, int], f: str, l: str) -> None:
    cursor = conn.cursor()

    e = 'NULL' if e in (None, '') else e

    try:
        '''
        Creates a new entry in the db.
        Required two cases as the email field is op
        '''
        if e != 'NULL':
            cursor.execute(f"""
                INSERT INTO users (username,passwd,email_id,first_name,last_name)
                VALUES ('{u}','{p}','{e}','{f}','{l}');
                """)
        else:
            cursor.execute(f"""
            INSERT INTO users (username,passwd,email_id,first_name,last_name)
            VALUES ('{u}','{p}',{e},'{f}','{l}');
            """)

        conn.commit()

    except ConnectionError:
        Popup("Error Connecting to Database.",
              "Please try again or restart the program")

    cursor.close()


def get_income_and_expense(user: str) -> Tuple[float, float]:
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT SUM(amount) 
        FROM transactions 
        WHERE 
        exp_date BETWEEN '{year}-{month}-01' AND '{year}-{month}-31' 
        AND exp_type = 'CR';""")

    try:
        income = cursor.fetchone()[0]
    except TypeError:
        print("No records found. Setting income to None")
        income = None

    cursor.execute(f"""
        SELECT SUM(amount) 
        FROM transactions 
        WHERE 
        exp_date BETWEEN '{year}-{month}-01' AND '{year}-{month}-31' 
        AND exp_type = 'DR' 
        AND username = '{user}';""")

    try:
        expense = cursor.fetchone()[0]
        if expense == None:
            expense = 0

    except TypeError:
        print("No records found. Setting expense to None")
        expense = None

    cursor.close()

    return (income, expense)


def get_user_details(user: str) -> List[str]:
    cursor = conn.cursor()

    cursor.execute(f"""
    SELECT user_id,username,passwd,email_id,first_name,last_name
    FROM users
    WHERE username = '{user}';
    """)

    user_details = cursor.fetchall()

    cursor.close()

    return user_details


def username_used(user: str) -> bool:
    cursor = conn.cursor()

    cursor.execute(f"""
    SELECT COUNT(username) FROM users
    WHERE username = '{user}';
    """)

    user_count = cursor.fetchone()[0]

    if user_count != 0:
        return False
    else:
        return True


def get_transactions(user: Union[str,int]) -> List[Tuple]:
    cursor = conn.cursor()

    cursor.execute(f"""
    SELECT particulars,exp_type,amount,exp_date
    FROM transactions
    WHERE username = '{user}' OR user_id = {user};
    """)

    transactions : List[Tuple] = cursor.fetchall()
    
    return transactions
# <----------------------- GUI -----------------------------> #

#   ________  ___  ___  ___
#  |\   ____\|\  \|\  \|\  \
#  \ \  \___|\ \  \\\  \ \  \
#   \ \  \  __\ \  \\\  \ \  \
#    \ \  \|\  \ \  \\\  \ \  \
#     \ \_______\ \_______\ \__\
#      \|_______|\|_______|\|__|

'''
Why am I using a class to store all my GUI functions? 

-> So that I could use locally created values like vals and user_details within other functions
   and to prevent me from getting a headache while managing scopes.

No, seriously though, making an object really helps while handling local objects as globals, making the programming
enjoyable and painless.
'''

class Xpnsit:
    def Login(self):
        login_active = True
        layout = [
            [T("Xpnsit", **heading_format)],
            [T("Username:"), Input(key="user")],
            [T("Password:"), Input(key="pass", password_char='*')],
            [Button("Login"), Button("Signup")]
        ]

        win = Window("Xpnsit", layout=layout)

        while login_active:  # <------------ Event Loop -----------------> #
            event, values = win.Read()

            if event is None:
                print("Exiting event loop")
                login_active = False

            if event == "Login":
                success = check_login_info(values["user"], values["pass"])

                if success == True:
                    print("Login Successful.")
                    self.user = values["user"]
                    login_active = False
                    # dash_active = True
                    win.close()
                    self.Interface()

            if event == "Signup":
                self.Signup()

    def Signup(self):
        signup_active = True

        layout = [
            [T("Signup for Xpnsit", **heading_format), ],
            [T("First Name:"), Input(key="f_name"), T(
                " "), T("Last Name:"), Input(key="l_name")],
            [T("Username:", justification='center'), Input(key="user")],
            [T("Password:", justification='center'), Input(key="pass")],
            [T("E-mail (Optional):", justification='center'), Input(key="mail")],
            [],
            [T(' '*40), Submit()]
        ]

        signup_win = Window("Xpnsit - Signup", layout=layout)

        while signup_active:  # <------------ Event Loop -----------------> #
            event, values = signup_win.Read()

            if event in (None, 'Exit'):
                signup_active = False
                login_active = True

            if event == 'Submit':
                self.vals = [values["user"], values["pass"],
                             values["mail"], values["f_name"], values["l_name"]]
                if not username_used(self.vals[0]):
                    create_account(*self.vals)

                    # <------------------- Confirmation of Insertion ------------------> #
                    success = check_login_info(values["user"], values["pass"])

                    if success == True:
                        print("Signup Successful.")
                        Popup(
                            "Signup Successful!",
                            "Exit this popup to return to the login page"
                        )
                        signup_active = False
                        login_active = True
                else:
                    PopupError("ERROR: Username already in usage",
                               title="Username already taken")

    def Dashboard(self):
        income, expenses = get_income_and_expense(self.user)
        self.user_details = get_user_details(self.user)

        if (income, expenses) == (None, None):
            dash_layout = [
                [T(f"Welcome {self.user_details[0][3]}")],
                [T("Looks like you have no transactions!\nGo add one in the Transactions tab.",justification="center")],
                [T("-"*40, text_color="gray")],
            ]
        else:
            dash_layout = [
                [T(f"Welcome {self.user_details[0][3]}")],
                [T(f"Your expenses for {months[month]}-{year} are:"),
                 T(str(expenses), font=("Arial", 20))],
                [T(f"Your income for {months[month]}-{year} is:"),
                 T(str(income), font=("Arial", 20))],
                [T("-"*40, text_color="gray")],
                [T("Net Profit/Loss:", font=("Segoe", 18)),
                 T(str(income-expenses), font=("Arial", 24))]
            ]

        dash_active = True

        return dash_layout

    def Transactions(self):
        transaction_layout = [
            [T("Under Construction!")]
        ]

        return transaction_layout

    def Analysis(self):
        analysis_layout = [
            [T("Under Construction!")]
        ]

        return analysis_layout

    def Interface(self):
        layout = [
            [T("Xpnsit", **heading_format)],
            [TabGroup([
                [
                    Tab("Dashboard", self.Dashboard(
                    ), tooltip="See an overview of your account", font=("Arial", 12)),
                    Tab("Transactions", self.Transactions(
                    ), tooltip="View,add and delete transactions", font=("Arial", 12)),
                    Tab("Analysis", self.Analysis(
                    ), tooltip="Get a graphical insight to your spendings.", font=("Arial", 12))
                ]
            ],)]
        ]

        win = Window("Xpnsit v1.0", layout=layout,size=(400,400))
        while True:
            event,values = win.Read()
            if event in (None,'Exit'):
                win.close()
                break
            
            


# <---------- MAIN: Calls an instance of the Xpnsit class and starts off with the Login page --------> #
if __name__ == "__main__":
    main_win = Xpnsit()

    main_win.Login()
