from __init__ import *
from login import login_cursor
# import easygui as gui
import PySimpleGUI as sg


# msg = "Welcome to Xpnsit, the best way to manage your expenses! To begin, login or signup below"
# title = 'Xpnsit v0.1'
# login_fields = ['Username','Password']
# gui.Popup(msg,title = title)



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

while True:
    event, values = login_window.Read()

    if event is None or event == 'Exit':
        break

    elif event == 'Login':
        print(event,values)

        u_name = values['_name_']
        pwd = values['_password_']

        login_cursor.execute(f"select username,passwd from users;")

        if (u_name,pwd) in login_cursor.fetchall():
            login_window.Close()

            dash_active = True

            dashboard_layout = [
                                [sg.Text("XPNSIT", font = ("Arial", 30), justification='center')],
                                [sg.Button('Manage Transactions',size = (10,3)), sg.Button('Notebook', size = (10,3))], sg.Text("Welcome to Xpnsit, {}! Take a look around to make yourself at home".format(u_name))],
                                [sg.T('')],
                                [sg.Button('Analytics', size = (10,3)), sg.Button('Transaction History', size = (10,3))]

                               ]
            dashboard = sg.Window('Dashboard - Xpnsit v0.1', dashboard_layout,default_button_element_size=(10, 3), size = (512,200),text_justification='center')

            # dashboard.Finalize()

            # dashboard.Enable()
            break
        else:
            sg.PopupError("Invalid username or password. Please try again.", title = 'Error')

while True:
    event2, values2 = dashboard.Read()

    if event2 is None or event2 == 'Exit':

        break

# auth()

# dashboard.Disable()
