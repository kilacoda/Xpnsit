# confirm = [
#     [sg.Text('Confirm signup?')],
#     [sg.Text('       '),sg.Button('Yes'),sg.Button('No')]
# ]
# confirm_win = sg.Window(confirm)
# # c_active = True

# c_event, c_val = confirm_win.Read(timeout=0)
# if c_event is None or c_event == 'No':
#     confirm.Close()
# elif c_event == 'Yes':

import PySimpleGUI as sg

vals = [[1,2,3]]
heads = ['a','b','c']
lt = [
    [sg.Text('Does this work?')],
    [sg.Table(vals,heads,auto_size_columns = False)]
]
window = sg.Window('Tables', resizable = True).Layout(lt)
while True:
    print(window.Read())

    event,values = window.Read()
    print(event,values)
    if event is None:
        break

# #!/usr/bin/env python
# import sys
# import PySimpleGUI as sg


# def make_table(num_rows, num_cols):
#     data_values = [[]]
#     column_lables = ['Day', 'Sunday', 'Monday',
#                      'Tuesday', 'Wednesday', 'Thursday']
#     for i in range(num_rows):
#         row_values = [sg.T('{}'.format(column_lables[i]), size=(11, 1), justification='right')] + [sg.InputText(
#             '', size=(10, 1), pad=(1, 1), justification='right', key=(i, j), do_not_clear=True) for j in range(num_cols)]
#         data_values.append(row_values)
# #    char = ''
# #    data = [[char for j in range(num_cols)] for i in range(num_rows)] # initializating
#     return data_values


# data = make_table(num_rows=6, num_cols=6)
# print(type(data))
# # sg.SetOptions(element_padding=(0,0))
# headings = ['Day', 'No Answer Dials',
#             'Contacts', 'Appt.', 'social', 'Call Backs']
# print(headings)

# layout = [[sg.Table(data[1:][:], headings=headings, max_col_width=25,
#                     auto_size_columns=True, display_row_numbers=False, justification='right', num_rows=7, alternating_row_color='lightblue', key='_table_')],
#           [sg.Button('Read')],
#           [sg.T('Read = read which rows are selected')]]

# window = sg.Window('Table', grab_anywhere=False, resizable=True).Layout(layout)

# while True:
#     event, values = window.Read()
#     if event is None:
#         break
#     sg.Popup(event, values)
#     # print(event, values)
# window.Close()
# sys.exit(69)


# import PySimpleGUI as sg

# values = [['1', '2', '3'], ['4', '5', '6']]
# header = values[0]
# usersTab = [[sg.Button('     ', key='Add User', button_color=sg.TRANSPARENT_BUTTON, border_width=0, )],
#             [sg.Table(values=values, auto_size_columns=False, headings=header)]]
# logsTab = [[sg.T('Test Logs')]]

# adminMainLayout = [
#     [sg.TabGroup([[sg.Tab('Users', usersTab), sg.Tab('Logs', logsTab)]])]]

# layout = adminMainLayout

# window = sg.Window('My window', border_depth=0).Layout(layout)

# window.Read()





















