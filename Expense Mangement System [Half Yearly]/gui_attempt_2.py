from __init__ import *
from login import login_cursor
import PySimpleGUI as sg
import numpy as np
import itertools
# from Layouts import *
def drange(start, stop, step):
    numelements = int((stop-start)/float(step))
    for i in range(numelements+1):
            yield start + i*step


####################################################### Login Area #################################################################

login_window = sg.Window('Xpnsit v0.1')

space1 = '                                   '  ## Tabs so that I could justify the fields and buttons
space2 = '                                                                                       '

layout = [
          [sg.Text('Welcome to Xpnsit, the best way to manage your expenses! To begin, login or signup below.',font = ('Helvetica',15),justification='center')],
          [sg.T(space1),sg.Text('Username', size=(15, 1)), sg.InputText(key='_name_')],
          [sg.T(space1),sg.Text('Password', size=(15, 1)), sg.InputText(key='_password_',password_char = '*')],
          [sg.T('')],
          [sg.T(space2),sg.Button('Login', tooltip='Login',bind_return_key=True), sg.Button('Signup',tooltip='Signup (if you haven\'t already)')]
         ]
login_window.Layout(layout)

# dashboard.Layout(dashboard_layout)

    # global login_window,dashboard
dash_active = False

##################################################### Calling the login window and starting an event loop ########################################

while True:
    event, values = login_window.Read()

    if event is None or event == 'Exit':
        break

    if not dash_active and event == 'Login':
        # dash_active = True
        print(event,values)

        u_name = values['_name_']
        pwd = values['_password_']

        login_cursor.execute(f"select username,passwd from users;")

        if (u_name,pwd) in login_cursor.fetchall():
            login_window.Close()

##################################################### From here begins the dashboard page #####################################

            dash_active = True

            dashboard_butt_col_layout = [
                                [sg.Text("XPNSIT", font = ("Arial", 30), justification='center')],
                                [sg.Button('Manage Transactions',size = (10,3)), sg.Button('Notebook', size = (10,3))],
                                [sg.Button('Analytics', size = (10,3)), sg.Button('Transaction History', size = (10,3))],


                               ]

            dash_layout = [
                            [sg.Column(dashboard_butt_col_layout),sg.VerticalSeparator()],
                            [sg.Text("Welcome to Xpnsit, {}!".format(u_name) )],
                            [sg.Text(" Take a look around to make yourself at home")],
                            [sg.T('')]
            ]
            dashboard = sg.Window('Dashboard - Xpnsit v0.1', dash_layout,default_button_element_size=(10, 3), size = (512,200),text_justification='center')

            # dashboard.Finalize()

            # dashboard.Enable()
            break
        else:
            sg.PopupError("Invalid username or password. Please try again.", title = 'Error')
newTransActive = False
notebookActive = False
analyticsActive = False
historyActive = False

#################################################### Event loop which corresponds to each button function #############################################





while True:
    event2, values2 = dashboard.Read(timeout = 1000)

    # if event2 is None or event2 == 'Exit':
    #     break

    if not newTransActive and event2 == 'Manage Transactions':


        newTransActive = True
        # range_array = np.arange(0,1000000,0.01)
        # spinRange = [i/100 for i in range(0,100000000)]
        # print(spinRange)

        new_trans_layout = [
                    [sg.Text(space1), sg.Txt("New Transaction")],
                    [sg.T('')],
                    [sg.Text('Name/Particulars'), sg.Input()],
                    [sg.Text('Amount'), sg.Spin(drange(0,1000000000,0.01),initial_value=0.00)],
                    [sg.Text('Type'), sg.InputCombo(['Income','Expense'])],
                    [sg.Text('Date of Transaction'), sg.CalendarButton(button_text="Select Date", key = '_cal_'), sg.Text('   ', key = '_OUTPUT_')],
                    ]

        new_trans = sg.Window('New Transaction', new_trans_layout, keep_on_top=False)


while True:
    nt_event,nt_values = new_trans.Read(timeout=1000)
    new_trans.FindElement('_OUTPUT_').Update(nt_values['_cal_'])
    print(nt_values,nt_values['_cal_'] )

            # if nt_event == 'Exit':
            #     newTransActive = False
            #     new_trans.Close()
