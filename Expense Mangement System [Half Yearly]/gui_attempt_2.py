from __init__ import *
from login import login_cursor
import PySimpleGUI as sg
import datetime


####################################################### Login Area #################################################################

# login_window = sg.Window('Xpnsit v0.1')

space1 = '                                   '  ## Tabs so that I could justify the fields and buttons
space2 = '                                                                                       '

newTransActive = False
notebookActive = False
analyticsActive = False
historyActive = False

layout = [
          [sg.Text('Welcome to Xpnsit, the best way to manage your expenses! To begin, login or signup below.',font = ('Helvetica',15),justification='center')],
          [sg.T(space1),sg.Text('Username', size=(15, 1)), sg.InputText(key='_name_')],
          [sg.T(space1),sg.Text('Password', size=(15, 1)), sg.InputText(key='_password_',password_char='*')],
          [sg.T('')],
          [sg.T(space2), sg.Button('Login', tooltip='Login', bind_return_key=True), sg.Button('Signup',tooltip='Signup (if you haven\'t already)')]
         ]
login_window = sg.Window('Xpnsit v0.1').Layout(layout)

dash_active = False

# Calling the login window and starting an event loop
i = 0

while True:
    try:
        event, values = login_window.Read(timeout=100)
    except :
        pass

    if event != sg.TIMEOUT_KEY:
        print(i, event, values)

    if event is None or event == 'Exit':
        break

    elif event == 'Login' and not dash_active:
        # dash_active = True
        print(event,values)

        u_name = values['_name_']
        pwd = values['_password_']

        login_cursor.execute(f"select username,passwd from users;")

        if (u_name,pwd) in login_cursor.fetchall():
            login_window.Close()

#    __From here begins the dashboard page__
            details = conn.cursor()
            details.execute(f"select * from users where username = '{u_name}'")
            current_user_details = details.fetchall()
            dash_active = True

            dashboard_butt_col_layout = [
                                [sg.Text("XPNSIT", font = ("Arial", 30), justification='center')],
                                [sg.Button('Manage Transactions',size=(10,3)), sg.Button('Notebook', size = (10,3))],
                                [sg.Button('Analytics', size=(10,3)), sg.Button('Transaction History', size = (10,3))],


                               ]

            dash_layout = [
                            [sg.Column(dashboard_butt_col_layout),sg.VerticalSeparator()],
                            # [sg.Text("Welcome to Xpnsit, {}!".format(u_name) )],
                            # [sg.Text(" Take a look around to make yourself at home")],
                            # [sg.T('')]
            ]
            dashboard = sg.Window('Dashboard - Xpnsit v0.1', dash_layout,default_button_element_size=(10, 3),
                                  size=(512, 200), text_justification='center')
            # break
        else:
            sg.PopupError("Invalid username or password. Please try again.", title = 'Error')

# Event loop which corresponds to each button function
    if dash_active:

        event, values = dashboard.Read()

        if event != sg.TIMEOUT_KEY:
            print('Dashboard', event)
        # breakpoint()
        # imwatchingyou.refresh_debugger()
        if event == 'Exit' or event is None:
            dash_active = False
            dashboard.Close()

        if event == 'Manage Transactions' and not newTransActive:
            newTransActive = True

            new_trans_layout = [
            [sg.Text(space1), sg.Txt("New Transaction")],
            [sg.T('')],
            [sg.Text('Name/Particulars'), sg.Input()],
            [sg.Text('Amount'), sg.Spin([i for i in range(0, 1000000)], initial_value=0.00, key='whole'), sg.T('.'),sg.Spin([a for a in range (00,100)], key = 'deci', initial_value=00)],
            [sg.Text('Type'), sg.InputCombo(['Income','Expense'])],
            [sg.Text('Date of Transaction'), sg.CalendarButton(button_text="Select Date", key = '_cal_'), sg.Text('', key = '_OUTPUT_',auto_size_text=True)],
            [sg.Button("Submit"),sg.T('                     '),sg.Button('Exit')]
            ]

            new_trans = sg.Window('New Transaction', new_trans_layout)

            while True:
                nt_event, nt_values = new_trans.Read(timeout=100)

                print(nt_event, nt_values)
                # imwatchingyou.refresh_debugger()
                if nt_event is None or nt_event == 'Exit':
                    print('Exited from the New Transaction window')
                    newTransActive = False
                    new_trans.Close()
                    dashboard.Refresh()
                    # break;

                if nt_event == 'Select Date':
                    # newTransActive = True
                    print(nt_values['_cal_'] )
                    ################################################# Dates: For verifying that the user hasn't put a date AHEAD of time##################################################

                    dated_date = nt_values['_cal_']
                    todays_date = datetime.date.today()

                    if dated_date < todays_date:
                        new_trans.FindElement('_OUTPUT_').Update(nt_values['_cal_'])
                    else:
                        sg.PopupError(f"Please enter valid date (Today's date : {todays_date})")

                elif nt_event == 'Submit':
                    # newTransActive = True
                    confirm = sg.PopupYesNo('Confirm Operation?', title='Confirmation')
                    confirm_win = sg.Window(confirm)
                    # c_active = True

                    c_event , c_val = confirm_win.Read(timeout = 1000)
                    if c_event is None or c_event == 'No':
                        confirm.Close()
                        break
                    if c_event == 'Yes':
                        amt = str(nt_values['whole']) + '.' + str(nt_values['deci'])
                        with current_user_details as cud:
                            nt_cursor = conn.cursor()
                            nt_cursor.execute(f"insert into transactions values ({cud[0][0]}, {cud[0][1]}, {nt_values.values()[0]}, {nt_values.values()[1]}, {amt} , {nt_values['_cal_']} );")
                            conn.commit()
                            new_trans.Close()
                            newTransActive = False
                            # c_active = False
