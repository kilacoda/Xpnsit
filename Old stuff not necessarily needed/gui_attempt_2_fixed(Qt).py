from __init__ import *
from login import login_cursor
import PySimpleGUIWx as sg
import datetime
import matplotlib.pyplot as plt
'''
 NOTE (25-06-2019; 00:30): Use the layout from the multi_window.py file and modify it to the application's requirement. The thing is, that's working.
 And I think one of the major causes for my crashes is that I just haven't implemented it properly (e.g. the timeouts for the second ('Signup') window and the active flags). So, I'll try to get this up and running in about a week or so, if I'm lucky. Wish me luck! Also, don't worry, Raghav, it'll work eventually, and you're going to be smashing others projects in the face in the end. Believe in yourself. I'll go to sleep now, its 00:40. I'll have another go at this in the morning.

'''
'''
TODO (29/06/2019 19:46): Divide the dashboard and signup sections into seperate functions and call them in the main event loop.
'''


def strike(text):
    result = ''
    for c in text:
         result = result + c + '\u0336'
    return result


seven_july = '7th July'

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Function to check existance of a username, could be expanded for other values as well.#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def check_of_existence_of(username):
    name_check = conn.cursor()
    name_check.execute(f"select username from users;")
    if (username) in name_check.fetchall():
        return False
    else:
        return True


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Sort of debugging tool to find the status of the windows. #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def show_status_of(var):
    if var is signup_active:
        print(f"Signup Active = {signup_active}")
    elif var is dash_active:
        print(f"Dashboard Active = {dash_a}")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Function to update the table, used in 'Transaction History' only. #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def update_table(_query):
        try:
            hist_cursor.execute(_query)
            history.Element('table').Update(hist_cursor.fetchall())
            history.Refresh()
        except:
            print('Looks like you can\'t do something like this')


user_fields = '(username,passwd,email_id,first_name,last_name)'
# login_window = sg.Window('Xpnsit v0.1')

# Tabs so that I could justify the fields and buttons
space1 = '                                   '
space2 = '                                                                                       '

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Window states -> A check that's been applied so two instances of the same window don't occur. #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

newTransActive = False
notebookActive = False
analyticsActive = False
historyActive = False
dash_active = False
signup_active = False

# # # # # # # #
# Handy dates #
# # # # # # # #

today_date = str(datetime.date.today())
year = int(today_date[0:4])
month = int(today_date[5:7])
day = int(today_date[9:])

sg.ChangeLookAndFeel('NeutralBlue')

tooltips = [
    'Log a new transaction',
    'Quickly jot down transactions and make calculations. Export them to a csv file',
    'View graphs of your expenditure and income history',
    'See all of your transactions'
]

# # # # # # # # # # # # # # # # # # # #
#             LOGIN AREA              #
# # # # # # # # # # # # # # # # # # # #

layout = [
    [sg.Text('Welcome to Xpnsit, the best way to manage your expenses! To begin, login or signup below.', font=(
        'Helvetica', 15), justification='center')],
    [sg.T(space1), sg.Text('Username', size=(15, 1)),
     sg.InputText(key='_name_')],
    [sg.T(space1), sg.Text('Password', size=(15, 1)),
     sg.InputText(key='_password_', password_char='*')],
    [sg.T('')],
    [sg.T(space2), sg.Button('Login', tooltip='Login', bind_return_key=True),
     sg.Button('Signup', tooltip='Signup (if you haven\'t already)')]
]
login_window = sg.Window('Xpnsit v0.1').Layout(layout)


# Calling the login window and starting an event loop
i = 0

while True:
    # if not dash_active or not signup_active:
    event, values = login_window.Read(timeout=100)

    if event != sg.TIMEOUT_KEY:
        print(i, event, values)

    if event is None or event == 'Exit':
        break

    if event == 'Signup' and not signup_active:

        signup_active = True
        signup_layout = [
            [sg.Text('Signup', justification='center', font='Verdana, 15')],
            [sg.Text('Fields marked with an asterisk (*) are compulsory')],
            [sg.Text('Username * :'), sg.Input(do_not_clear=False,
                                               key='u_name'), sg.Text('                       ', key='name_check')],
            [sg.Text('Password * :'), sg.Input(do_not_clear=False,
                                               key='pass', password_char='*')],
            [sg.Text('Confirm Password * :'), sg.Input(do_not_clear=False,
                                                       key='pass_conf', password_char='*'), sg.Text('        ', key='pass_check')],
            [sg.Text('E-mail ID :'),
             sg.Input(do_not_clear=False, key='email')],
            [sg.Text('First Name * :'),
             sg.Input(do_not_clear=False, key='fname')],
            [sg.Text('Last Name * :'),
             sg.Input(do_not_clear=False, key='lname')],
            [sg.Button('Cancel'), sg.Text(space1), sg.Button(
                'Create account', button_color=('white', '#008000'))]
        ]

        signup = sg.Window('Signup').Layout(signup_layout)

        # signup.UnHide()
        # login_window.Hide()

        # break

    if not dash_active and event == 'Login':
        # dash_active = True
        print(event, values)

        u_name = values['_name_']
        pwd = values['_password_']

        login_cursor.execute(f"select username,passwd from users;")

        if (u_name, pwd) in login_cursor.fetchall():
            login_window.Hide()
            dash_active = True

#    __From here begins the dashboard page__
            details = conn.cursor()
            details.execute(f"select * from users where username = '{u_name}'")
            current_user_details = cud = details.fetchall()
            '''
            TODO:Change the layout such that it shows the users transaction history on login, and having the other functions in or tabs to the side. Yes, it'll be a pain in the arse, but the current layout looks hideously preposterous, you can't deny that. I'll keep this as a todo till I first figure out the functions themselve and create at least a working model of the app. (25/06/2019 15:04)
            '''
            dashboard_butt_col_layout = [
                [sg.Text("XPNSIT", font=("Helvetica", 25),
                         justification='center')],
                [sg.Button('Manage Transactions', size=(10, 3), tooltip=tooltips[0]),
                 sg.Button('Notebook', size=(10, 3), tooltip=tooltips[1])],
                [sg.Button('Analytics', size=(10, 3), tooltip=tooltips[2]), sg.Button(
                    'Transaction History', size=(10, 3), tooltip=tooltips[3])],


            ]

            dash_layout = [
                [sg.Column(dashboard_butt_col_layout)],
                # [sg.Text("Welcome to Xpnsit, {}!".format(u_name) )],
                # [sg.Text(" Take a look around to make yourself at home")],
                # [sg.T('')]
            ]
            dashboard = sg.Window('Dashboard - Xpnsit v0.1', dash_layout, default_button_element_size=(10, 3),
                                  size=(512, 200), text_justification='center')
            # break
        else:
            sg.PopupError(
                "Invalid username or password. Please try again.", title='Error')


# Event loop which corresponds to each button function

    ##########
    # Signup #
    ##########

    if signup_active:
        butt_event_signup, sign_details = signup.Read(timeout=0)

        if butt_event_signup != sg.TIMEOUT_KEY:
            print('Signup Event -->', butt_event_signup)
            print(butt_event_signup, sign_details)

        if butt_event_signup == 'Cancel' or butt_event_signup is None:
            # login_window.UnHide()
            signup_active = False
            signup.Hide()
            # break

        if check_of_existence_of(sign_details['u_name']) is True:
            signup.FindElement('name_check').Update('Available!')
        else:
            signup.FindElement('name_check').Update(
                'Username taken already')

        if butt_event_signup == 'Create account':
            sign_dets = []
            dets = ''

            if sign_details['email'] == '':
                sign_details['email'] = 'NULL'

            correct_info = False

            for (key, value) in sign_details.items():
                if value == '' and (key != 'email' or 'pass_conf'):
                    correct_info = False
                    error = 'incorrect_vals'
                    break

                elif key == 'pass_conf':
                    if value != sign_details['pass']:
                        correct_info = False
                        error = 'no_pass_match'
                        break
                else:
                    correct_info = True
                print(sign_dets)

            if correct_info == True:
                for (key, value) in sign_details.items():
                    if key not in ('pass_conf', 'name_check', 'pass_check'):
                        sign_dets.append(value)
                        if key != 'u_name':
                            dets = dets + ',' + repr(value)
                        else:
                            dets += repr(value)
                        print(dets)

                query = f'insert into users {user_fields} values ({dets});'
                print(query)
                signup_cursor = conn.cursor()
                signup_cursor.execute(query)
                conn.commit()

                if check_of_existence_of(sign_details['u_name']):
                    lt = [
                        [sg.Text('Signup Success!')],
                        [sg.Button('Return to Login')]
                    ]
                    success = sg.Window('Success', lt)
                    while True:
                        s_eve, s_val = success.Read()
                        if s_eve == 'Return to Login' or s_eve is None:
                            success.Close()
                            signup.Hide()
                            login_window.UnHide()
                            signup_active = False
                            break

            elif correct_info == False and error == 'incorrect_vals':
                signup_active = False
                sg.PopupError('Please fill required fields')

            elif correct_info == False and error == 'no_pass_match':
                signup_active = False
                sg.PopupError("Passwords don't match")

    #############
    # Dashboard #
    #############

    if dash_active:

        '''
        TODO: Make the second dashboard column a sort of mini guide about what the button leads to. Look for some on_hover function if available and link it to the button and button info 
        '''
        dash_event, values = dashboard.Read()

        if dash_event != sg.TIMEOUT_KEY:
            print('Dashboard', dash_event)

        if dash_event == 'Exit' or dash_event is None:
            dash_active = False
            dashboard.Close()
            login_window.UnHide()

        #############################
        # New/Manage Transaction(s):-
        #############################
        elif not newTransActive and dash_event == 'Manage Transactions':
            newTransActive = True
            dash_active = False
            dashboard.Hide()

            new_trans_layout = [
                [sg.Text(space1), sg.Txt("New Transaction")],
                [sg.T('')],
                [sg.Text('Name/Particulars:'), sg.Input()],
                [sg.Text('Amount:'), sg.Input(do_not_clear=True, default_text='0', size=(10, 2), key='whole'), sg.T(
                    '.'), sg.Input(do_not_clear=True, default_text='00', size=(10, 2), key='deci')],
                [sg.Text('Type:'), sg.InputCombo(
                    ['Income', 'Expense'], key='type', readonly=True)],
                [sg.Text('Date of Transaction:'), sg.CalendarButton(button_text=None, target='date', format='%Y-%m-%d', default_date_m_d_y=(month, day, year), key='calendar',
                                                                    image_filename='git\Xpnsit\Expense Mangement System [Half Yearly]\calendar1.png', image_subsample=20), sg.Text("       ", size=(15, 1), key='date')],
                [sg.Button("Enter"), sg.T(
                    '                     '), sg.Button('Exit')]
            ]

            new_trans = sg.Window('New Transaction', new_trans_layout)

        ############
        # Notebook :-
        ############

        elif not notebookActive and dash_event == 'Notebook':
            sg.Popup('Under construction!', 'Deadline ' + strike(seven_july))

        #############
        # Analytics :-
        #############

        elif not analyticsActive and dash_event == 'Analytics':
            sg.Popup('Under construction!', 'Deadline ' + strike(seven_july))

        #######################
        # Transaction History:-
        #######################

        elif not historyActive and dash_event == 'Transaction History':
            historyActive = True
            dash_active = False
            dashboard.Hide()
            # sg.PopupAnimated('833.gif',message='Loading',)
            hist_cursor = conn.cursor()
            # param = 'particulars'
            hist_query = "select particulars,exp_type,amount,exp_date from transactions where user_id = 2 order by particulars desc;"
            hist_cursor.execute(hist_query)
            history_values = hist_cursor.fetchall()
            headings = ['Particulars', 'Type', 'Amount', 'Date']
            rec_no = len(history_values)

            ##right_click_menu = ['Delete','Modify']

            hist_lt = [
                [sg.T('Transaction History', font=("Helvetica", 25)), sg.T(space1), sg.T('Sort By:'), sg.Combo(['Name', 'Date', 'Amount', 'Type'], size=(
                    10, 1), auto_size_text=False, enable_events=True, key='sort', change_submits=True, readonly=True)],
                [sg.T('Number of records to be shown:'), sg.Slider(range=(0, len(history_values)),
                                                                   default_value=rec_no, orientation='h', enable_events=True, key='rec_slider')],
                [sg.Table(history_values, headings=headings,
                          enable_events=True, key='table')],
                [sg.Button('Back')]
            ]

            history = sg.Window('Transaction History', hist_lt)

    #############################
    # New/Manage Transaction(s):-   (Layout on line 280 or somewhere around there)
    #############################
    if newTransActive:
        nt_event, nt_values = new_trans.Read()
        print(nt_event, nt_values)
        # imwatchingyou.refresh_debugger()
        if nt_event is None or nt_event == 'Exit':
            print('Exited from the New Transaction window')
            newTransActive = False
            dash_active = True
            new_trans.Close()
            dashboard.UnHide()

        # newTransActive = True
        if 'date' in nt_values.keys():
            print(nt_values['date'])
        else:
            continue

        ######################################################################
        # Dates: For verifying that the user hasn't put a date AHEAD of time #
        ######################################################################

        dated_date = repr(nt_values['date'])
        todays_date = repr(datetime.date.today())
        print(todays_date)
        if dated_date < todays_date:
            # nt_values['date'] = nt_values['date'].strftime()

            new_trans.FindElement('date').Update(
                nt_values['date'].strftime('%d-%m-&y'))
            print(nt_values['date'])
        elif dated_date > todays_date:
            error = 'invalid_date'
            sg.PopupError(
                f"Please enter valid date (Today's date : {todays_date})")

        if nt_values['type'] == 'Income':
            # nt_values['type'] = 'CR'
            exp_type = 'CR'
        elif nt_values['type'] == 'Expense':
            # nt_values['type'] = 'DR'
            exp_type = 'DR'

        if nt_event == 'Enter':
            amt = str(nt_values['whole']) + '.' + str(nt_values['deci'])
            nt_cursor = conn.cursor()
            trans_vals = list(nt_values.values())
            q = f"insert into transactions (user_id,username,particulars,exp_type,amount,exp_date) values ({cud[0][0]}, '{cud[0][1]}', '{trans_vals[0]}', '{exp_type}', {amt} , '{nt_values['date']}' );"
            print(q)
            try:
                nt_cursor.execute(q)
            except:
                sg.PopupError('Transaction not entered')

            conn.commit()
            vals = (cud[0][1], trans_vals[0], exp_type, float(amt))
            print(vals)
            temp_cursor = conn.cursor()
            query1 = f"select username,particulars,exp_type,amount from transactions where user_id = {cud[0][0]};"

            temp_cursor.execute(query1)
            fetch = temp_cursor.fetchall()
            for i in fetch:
                print(i)
            if vals == fetch[-1]:
                sg.Popup('Operation Successful!')
                newTransActive = False
                new_trans.Close()
                break
            else:
                sg.PopupError(
                    'Operation Cancelled due to technical failure.', 'Please try again')

    #######################
    # Transaction History:-
    #######################
    if historyActive:

        h_event, h_vals = history.Read()
        try:
            new_rec_no = int(h_vals['rec_slider'])
        except:
            pass
        if h_event != sg.TIMEOUT_KEY:
            print(h_event, h_vals)
        if h_event is None or h_event == 'Back':
            print('Exited from the Transaction History window')
            historyActive = False
            dash_active = True
            history.Close()
            dashboard.UnHide()

        elif h_event is not None or h_event != 'Back' and h_event == 'sort':
            if h_vals['sort'] == 'Name':
                hist_query = f"select particulars,exp_type,amount,exp_date from transactions where user_id = 2 order by particulars desc limit {new_rec_no};"

                update_table(hist_query)

            elif h_vals['sort'] == 'Amount':
                hist_query = f"select particulars,exp_type,amount,exp_date from transactions where user_id = 2 order by amount desc limit {new_rec_no};"
                update_table(hist_query)

            elif h_vals['sort'] == 'Date':
                hist_query = f"select particulars,exp_type,amount,exp_date from transactions where user_id = 2 order by exp_date desc limit {new_rec_no};"

                update_table(hist_query)

            elif h_vals['sort'] == 'Type':
               hist_query = f"select particulars,exp_type,amount,exp_date from transactions where user_id = 2 order by exp_type desc limit {new_rec_no} ;"
               update_table(hist_query)


login_window.Close()
