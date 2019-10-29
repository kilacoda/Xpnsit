# <------------------------ Imports ------------------------------> #
# <--- MySQL Errors ---> #
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import mysql.connector.errors as SQLErrors

# <--- Miscellenaeous ---> #
from typing import *
import csv
import datetime
import sys

# <--- Self-Defined stuff ---> #
from __init__ import conn, start_connection
from funcs import *

# <--- Matplotlib and PyPlot ---> #
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")

# <--- PySimpleGUI ---> #
if sys.version >= "3.0.0":
    import PySimpleGUI as sg
    from PySimpleGUI import Window, T, Input, Button, Popup, PopupError, Submit, TabGroup, Tab, Multiline, Combo, CalendarButton, Table, PopupYesNo, Canvas
else:
    import PySimpleGUI27 as sg
    from PySimpleGUI27 import Window, T, Input, Button, Popup, PopupError, Submit, TabGroup, Tab, Multiline, Combo, CalendarButton, Table, PopupYesNo, Canvas

# <------------------------- Useful Stuff ---------------------------------> #

tooltips = [
    'Log a new transaction',
    'Quickly jot down transactions and make calculations. Export them to a csv file',
    'View graphs of your expenditure and income history',
    'See all of your transactions'
]

heading_format = {
    "justification": 'center',
    "size":  (20, 1),
    "font":  ("Segoe", 20)
}

year = datetime.datetime.now().year
month = datetime.datetime.now().month
day = datetime.datetime.now().day

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

Here below lie all the MySQL related functions.
Queries, connectivity (actually in __init__.py, though), cursors, everything's here.
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
        Required two cases as the email field is optional
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
        AND exp_type = 'CR'
        AND username = '{user}';""")

    try:
        income = cursor.fetchone()[0]
        if income == None:
            income = 0
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

    user_details = cursor.fetchall()[0]

    cursor.close()

    return user_details


def username_used(user: str) -> bool:
    cursor = conn.cursor()

    cursor.execute(f"""
    SELECT COUNT(username) FROM users
    WHERE username = '{user}';
    """)

    user_count = cursor.fetchone()[0]
    print(f"No. of users with username {user} = {user_count}")
    if user_count != 0:
        return True
    else:
        return False


def get_transactions(user: Union[str, int],
                     n: int = 10000,
                     start_date: str = f"{year}-{month}-1",
                     end_date: str = f"{year}-{month}-{day}",
                     asc_or_desc: str = "ASC",
                     orderer: str = "particulars") -> List[Tuple]:
    headings = [
        "Particulars",
        "Type",
        "Amount",
        "Date"
    ]

    cursor = conn.cursor()

    where_clause_part_1 = f"username = '{user}'" if type(
        user) is str else f"user_id = {user}"
    where_clause = where_clause_part_1 + f"""
    AND
    exp_date BETWEEN '{start_date}' AND '{end_date}'
    ORDER BY {orderer} {asc_or_desc}
    """

    # <------------ Counts number of transactions falling into the requirements and returns them to the slider ----------------> #
    query = f"""
    SELECT COUNT(*)
    FROM transactions
    WHERE {where_clause};
    """
    cursor.execute(query)

    number_of_records = cursor.fetchone()[0]

    cursor.reset()

    query = f"""
        SELECT particulars,exp_type,amount,exp_date
        FROM transactions
        WHERE {where_clause}
        """

    if number_of_records < n:
        limit = f" LIMIT {number_of_records};"
    else:
        limit = f" LIMIT {n};"

    cursor.execute(query+limit)

    transactions: List[Tuple] = cursor.fetchall()
    print(transactions)
    trans_table = Table(transactions, headings, key="table", right_click_menu=["Options", [
                        "Edit", "Delete"]], enable_events=True) if number_of_records != 0 else T("No records to display")

    return transactions, trans_table, number_of_records


# <-------------------- PyPlot -------------------------> #
def get_graph_values(start_date: str = f"{year}-{month}-1",
                     end_date: str = f"{year}-{month}-{day}",
                     exp_type: str = "Credit"
                     ):

    cursor = conn.cursor()
    q_cr = f"""
    SELECT particulars,amount 
    FROM transactions 
    WHERE 
    exp_date BETWEEN "{start_date}" AND "{end_date}" 
    AND exp_type = "CR";
    """

    q_dr = f"""
    SELECT particulars,amount 
    FROM transactions 
    WHERE 
    exp_date BETWEEN "{start_date}" AND "{end_date}" 
    AND exp_type = "DR";
    """

    q_all = f"""
    SELECT particulars,amount 
    FROM transactions 
    WHERE 
    exp_date BETWEEN "{start_date}" AND "{end_date}";
    """

    if exp_type == 'Credit':
        q = q_cr
    elif exp_type == 'Debit':
        q = q_dr
    elif exp_type == 'Both':
        q1 = q_cr
        q2 = q_dr

    else:
        q = q_all

    if exp_type in ("Credit", "Debit", "All"):
        cursor.execute(q)
        points = cursor.fetchall()
        x = np.arange(0, len(points))
        y = [point[1] for point in points]
        plt.plot(x, y)
    else:
        cursor.execute(q1)
        points_1 = cursor.fetchall()
        x1 = np.arange(0, len(points_1))
        y1 = [point[1] for point in points_1]

        cursor.reset()

        cursor.execute(q2)
        points_2 = cursor.fetchall()
        x2 = np.arange(0, len(points_1))
        y2 = [point[1] for point in points_2]

        plt.plot(x1, y1)
        plt.plot(x2, y2)
        plt.grid(True)

    fig = plt.gcf()
    fig_x, fig_y, fig_w, fig_h = fig.bbox.bounds

    return fig, fig_w, fig_h

# <------------------------------- Beginning of Matplotlib helper code -----------------------> #


def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg
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
    def __init__(self):
        self.app_state: bool = True

    # <------------------- Misc. Functions (Layouts and Updaters and stuff) --------------------> #

    def Add_Trans(self, particulars: str, _type: str, amount: float, date: str):
        cursor = conn.cursor()

        try:
            cursor.execute(f"""
            INSERT INTO transactions (
                user_id,
                username,
                particulars,
                exp_type,
                amount,
                exp_date
            )
            VALUES (
                {self.user.user_id},
                '{self.user.uname}',
                '{particulars}',
                '{_type}',
                {amount},
                "{date}"
                );
            """)

            conn.commit()

            Popup("Transaction successfully added.")
            self.win.Refresh()

        except SQLErrors.ProgrammingError:
            PopupError("ERROR: Invalid details.\nRectify and try again.")

        cursor.close()

    def Create_Add_Trans_Layout(self):
        layout = [
            [T("New Transaction", font=("Helvetica", 18))],
            [T("NOTE:", font=("Helvetica", 20)), T(
                "All fields are required to be filled.")],
            [T("Particulars:"), Multiline("Enter details of transaction",
                                          autoscroll=True, key="Particulars")],
            [T("Transaction type:"), Combo(["Select", "Credit", "Debit"],
                                           "Select", readonly=True, key="new_type")],
            [T("Amount:"), Input(enable_events=True, key="amount")],
            [T("Date Of Transaction:"), Input("YYYY-MM-DD or use the button on the right",
                                              key="date"), CalendarButton("Select Date", target="date", format="%Y-%m-%d")],
            [Submit()]
        ]

        return layout

    def History(self):
        history_values, table, no_of_records = get_transactions(
            self.user.uname)

        layout = [
            [T("Transaction History", font=("Helvetica", 18))],
            [T("All your transactions, in one place. Right click any one to delete or edit it.")],
            [sg.T('Number of records to be shown:'),
             sg.Slider(
                 range=(0, no_of_records),
                 default_value=no_of_records,
                 orientation='h',
                 enable_events=True,
                 key='slider'
            )
            ],
            [T("Show records from "),
             Input(f"{year}-{month}-1", key="start_date", size=(10, 1)),
             CalendarButton("Start date", target="start_date", default_date_m_d_y=(
                 month, 1, year), button_color=("white", "green"), format="%Y-%m-%d"),
             T("to"),
             Input(f"{year}-{month}-{day}", key="end_date", size=(10, 1)),
             CalendarButton("End date", target="end_date", default_date_m_d_y=(
                 month, day, year), button_color=("white", "red"), format="%Y-%m-%d")
             ],
            [T("Type:"), Combo(["All", "Credit", "Debit"],
                               default_value="All", key="used_type", readonly=True)],
            [T("Sort by:"), Combo(["Name", "Amount", "Date of Transaction"],
                                  default_value="Name", key="sort_by", readonly=True), Combo(["Ascending", "Descending"], default_value="Ascending", key="asc_or_desc", readonly=True)],
            [table, Button("Refresh", button_color=(
                "white", "orange"), bind_return_key=True, key="refresh")],


        ]
        self.history_active = True

        return layout

    def update_table(self):
        start, end = self.values['start_date'], self.values["end_date"]
        aod = 'ASC' if self.values["asc_or_desc"] == "Ascending" else "DESC"
        sort = "particulars" if self.values["sort_by"] == "Name" else "amount" if self.values["sort_by"] == "Amount" else "exp_date"

        new_trans, new_table, new_number_of_trans = get_transactions(
            self.user.user_id,
            int(self.values["slider"]),
            start,
            end,
            aod,
            sort
        )
        print(new_trans, new_table, new_number_of_trans)
        self.win["table"].Update(new_trans)
        self.win["slider"].Update(range=(0, new_number_of_trans))
        self.win.Refresh()
    # <------------------ Main Screens --------------------> #

    def Login(self):
        login_active = True
        layout = [
            [T("Xpnsit", **heading_format)],
            [T("Username:"), Input(key="user")],
            [T("Password:"), Input(key="pass", password_char='*')],
            [Button("Login", bind_return_key=True), Button("Signup")]
        ]

        win = Window("Xpnsit", layout=layout)

        while login_active:  # <------------ Event Loop -----------------> #
            event, values = win.Read()

            if event is None:
                print("Exiting event loop")
                login_active = False
                self.app_state = False
                win.close()
                del win
                break

            if event == "Login":
                success = check_login_info(values["user"], values["pass"])

                if success == True:
                    print("Login Successful.")

                    self.user_details = get_user_details(values["user"])
                    self.user = NewUser(*self.user_details)

                    win.close()

                    self.Interface()
                    login_active = False
                else:
                    PopupError(
                        "ERROR: Username or password incorrect.\nPlease try again.")

            if event == "Signup":
                self.Signup()

    def Signup(self):
        signup_active = True

        layout = [
            [T("Signup for Xpnsit", **heading_format), ],
            [T("First Name:"), Input(size=(15, 1), key="f_name"), T(
                " "), T("Last Name:"), Input(size=(15, 1), key="l_name")],
            [T("Username:", justification='center'),
             Input(size=(35, 1), key="user")],
            [T("Password:", justification='center'), Input(
                size=(35, 1), key="pass", password_char="*")],
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
                        signup_win.close()
                        signup_active = False
                        login_active = True
                else:
                    PopupError("ERROR: Username already in usage",
                               title="Username already taken")

    def Dashboard(self):
        income, expenses = get_income_and_expense(self.user.uname)

        if (income, expenses) == (None, None):
            dash_layout = [
                [T(f"Welcome {self.user.first_name}")],
                [T("Looks like you have no transactions!\nGo add one in the Transactions tab.",
                   justification="center")],
                [T("-"*60, text_color="gray")],
            ]
        else:
            dash_layout = [
                [T(f"Welcome {self.user.first_name}")],
                [T(f"Your expenses for {months[month-1]}-{year} are:"),
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
            [T("Transactions", font=("Helvetica", 18))],
            [TabGroup(
                [
                    [Tab("New Transaction", self.Create_Add_Trans_Layout())],
                    [Tab("History", self.History())]
                ]
            )]
        ]

        return transaction_layout

    def Analytics(self):
        fig, w, h = get_graph_values()

        analysis_layout = [
            [T("Analytics", font=("Helvetica", 18))],
            [T("Here you can find and generate graphs for your desired timeframe\nand observe trends in your balance.")],
            [T("Generate for records from "),
             Input(f"{year}-{month}-1", key="a_start_date", size=(10, 1)),
             CalendarButton("Start date", target="a_start_date", default_date_m_d_y=(
                 month, 1, year), button_color=("white", "green"), format="%Y-%m-%d"),
             T("to"),
             Input(f"{year}-{month}-{day}", key="a_end_date", size=(10, 1)),
             CalendarButton("End date", target="a_end_date", default_date_m_d_y=(
                 month, day, year), button_color=("white", "red"), format="%Y-%m-%d")
             ],
            [T("Type:"), Combo(["All", "Credit", "Debit", "Both"],
                               default_value="All", key="a_type", readonly=True)],
            [Button("Generate", button_color=("white", "orange"))],
            [Canvas(size=(w, h), key="canvas")]
        ]

        return analysis_layout

    def Interface(self):
        layout = [
            [T("Xpnsit", **heading_format), T(" "*50), Button("Settings"),
             Button("Log Out", button_color=("black", "yellow"))],
            [TabGroup([
                [
                    Tab("Dashboard", self.Dashboard(
                    ), tooltip="See an overview of your account", font=("Arial", 12)),
                    Tab("Transactions", self.Transactions(
                    ), tooltip="View,add and delete transactions", font=("Arial", 12), key="transactions"),
                    Tab("Analytics", self.Analytics(
                    ), tooltip="Get a graphical insight to your spendings.", font=("Arial", 12))
                ]
            ],)]
        ]

        self.win = Window("Xpnsit v1.0", layout=layout)
        while True:
            self.event, self.values = self.win.Read()

            if self.event in (None, 'Exit'):
                self.win.close()
                self.app_state = False
                break

            if self.event != sg.TIMEOUT_KEY:
                print(f"Event = {self.event}\nValues = {self.values}")

            if self.event == "Log Out":
                logout = PopupYesNo("Are you sure?")

                if logout == 'Yes':
                    sg.popup_quick_message(
                        "Okay, closing. Bye", auto_close_duration=4)
                    self.win.close()
                    # self.app_state = False
                    del self.win
                    break

            if self.event == "Submit":
                _type = "CR" if self.values["new_type"] in (
                    "Credit", "Select") else "DR"
                self.Add_Trans(
                    self.values["Particulars"],
                    _type,
                    self.values["amount"],
                    self.values["date"])

            if self.event in ("slider", "refresh"):

                self.update_table()
                self.win.refresh()

            if self.event == "Generate":
                fig, w, h = get_graph_values(
                    self.values['a_start_date'],
                    self.values['a_end_date'],
                    self.values["a_type"],
                    )
                figure_canvas_agg = draw_figure(self.win['canvas'].TKCanvas, fig)

class NewUser:
    def __init__(self, *details):
        self.user_id: int = details[0]
        self.uname: str = details[1]
        self.mail_id: str = details[3]
        self.first_name: str = details[4]
        self.last_name: str = details[5]
        self.full_name: str = self.first_name + ' ' + self.last_name
        self.state: bool = True


# <---------- MAIN: Calls an instance of the Xpnsit class and starts off with the Login page --------> #

if __name__ == "__main__":
    main_win = Xpnsit()
    # app_state = main_win.app_state
    while True:
        print(main_win.app_state)
        if main_win.app_state == True:
            main_win.Login()
        else:
            break
