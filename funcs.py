"""
22nd September, 2019 09:23 a.m.

This file has been made to clean up the main GUI file.
All functions can be imported using "from funcs import *"
"""


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# This function creates the layout for the transaction window or adds a line if no records present. #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def create_hist_layout():
    combo_kwargs = {size: (10, 1), auto_size_text: False, enable_events: True,
                    key: 'sort', change_submits: False, readonly: True}
    og_hist_lt = [
        [sg.T('Transaction History', font=("Helvetica", 25)), sg.T(space1), sg.T('Sort By:'), sg.Combo(
            ['Name', 'Date', 'Amount', 'Type'], **combo_kwargs)], sg.Combo(['Ascending', 'Descending'])
        [sg.T('Number of records to be shown:'), sg.Slider(range=(0, len(history_values)),
                                                           default_value=rec_no, orientation='h', enable_events=True, key='rec_slider')],
        [],
        [sg.Button('Back')]
    ]
    if rec_no != 0:
        og_hist_lt[2] = [
            sg.Table(history_values, headings=headings, enable_events=True, key='table')]
    else:
        og_hist_lt[2] = [sg.T("No records to display!")]

    return og_hist_lt

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

#######################
# Transaction History:-
#######################

def action_history():


    h_event, h_vals = history.Read()
    try:
        new_rec_no = int(h_vals['rec_slider'])
    except:
        # history.Element('table').Update(disabled = True)
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
            hist_query = f"{hist_query[:89]}particulars desc limit {new_rec_no};"

            update_table(hist_query)

        elif h_vals['sort'] == 'Amount':
            hist_query = f"{hist_query[:89]}amount desc limit {new_rec_no};"
            update_table(hist_query)

        elif h_vals['sort'] == 'Date':
            hist_query = f"{hist_query[:89]}exp_date desc limit {new_rec_no};"

            update_table(hist_query)

        elif h_vals['sort'] == 'Type':
            hist_query = f"{hist_query[:89]}exp_type desc limit {new_rec_no} ;"
            update_table(hist_query)
