# # """
# #     PySimpleGUI The Complete Course
# #     Lesson 7 - Multiple Windows
# # """
# # import PySimpleGUI as sg
# #
# # # Design pattern 2 - First window remains active
# #
# # layout = [[ sg.Text('Window 1'),],
# #           [sg.Input(do_not_clear=True)],
# #           [sg.Text('', key='_OUTPUT_')],
# #           [sg.Button('Launch 2'), sg.Button('Exit')]]
# #
# # win1 = sg.Window('Window 1').Layout(layout)
# #
# # win2_active = False
# # while True:
# #     ev1, vals1 = win1.Read(timeout=100)
# #     win1.FindElement('_OUTPUT_').Update(vals1[0])
# #     if ev1 is None or ev1 == 'Exit':
# #         break
# #
# #     if not win2_active and ev1 == 'Launch 2':
# #         win2_active = True
# #         layout2 = [[sg.Text('Window 2')],
# #                    [sg.Button('Exit')]]
# #
# #         win2 = sg.Window('Window 2').Layout(layout2)
# #
# #     if win2_active:
# #         ev2, vals2 = win2.Read(timeout=100)
# #         if ev2 is None or ev2 == 'Exit':
# #             win2_active  = False
# #             win2.Close()
#
#
import sys
if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI as sg

"""
    Demo - Running 2 windows with both being active at the same time
    Three important things to note about this design patter:
        1. The layout for window 2 is inside of the while loop, just before the call to window2=sg.Window
        2. The read calls have timeout values of 100 and 0.  You can change the 100 to whatever interval you wish
            but must keep the second window's timeout at 0
        3. There is a safeguard to stop from launching multiple copies of window2.  Only 1 window2 is visible at a time
"""

# Window 1 layout
layout = [
            [sg.Text('This is the FIRST WINDOW'), sg.Text('      ', key='_OUTPUT_')],
            [sg.Text('')],
            [sg.Button('Launch 2nd Window'),sg.Button('Popup'), sg.Button('Exit')]
         ]

window = sg.Window('Window Title', location=(800, 600)).Layout(layout)
win2_active = False
i = 0
while True:             # Event Loop
    event, values = window.Read(timeout=100)
    if event != sg.TIMEOUT_KEY:
        print(i, event, values)

    if event is None or event == 'Exit':
        break
    elif event == 'Popup':
        sg.Popup('This is a BLOCKING popup','all windows remain inactive while popup active')
    i += 1
    if event == 'Launch 2nd Window' and not win2_active:     # only run if not already showing a window2
        win2_active = True
        # window 2 layout - note - must be "new" every time a window is created
        layout2 = [
            [sg.Text('The second window'), sg.Text('', key='_OUTPUT_')],
            [sg.Input(do_not_clear=True, key='_IN_')],
            [sg.Button('Show'), sg.Button('Exit')]
                ]
        window2 = sg.Window('Second Window').Layout(layout2)
    # Read window 2's events.  Must use timeout of 0
    if win2_active:
        # print("reading 2")
        event, values = window2.Read(timeout=100)
        # print("win2 ", event)
        if event != sg.TIMEOUT_KEY:
            print("win2 ", event)
        if event == 'Exit' or event is None:
            # print("Closing window 2", event)
            win2_active = False
            window2.Close()
        if event == 'Show':
            sg.Popup('You entered ', values['_IN_'])

window.Close()


#
# import PySimpleGUI as sg
#
# layout = [[sg.Text('Window 1'), ],
#           [sg.Input(do_not_clear=True)],
#           [sg.Text('', key='_OUTPUT_')],
#           [sg.Button('Next >'), sg.Button('Exit')]]
#
# win1 = sg.Window('Window 1').Layout(layout)
#
# win3_active = win2_active = False
# while True:
#     if not win2_active:
#         ev1, vals1 = win1.Read()
#         if ev1 is None or ev1 == 'Exit':
#             break
#         win1.FindElement('_OUTPUT_').Update(vals1[0])
#
#     if not win2_active and ev1 == 'Next >':
#         win2_active = True
#         win1.Hide()
#         layout2 = [[sg.Text('Window 2')],
#                    [sg.Button('< Prev'), sg.Button('Next >')]]
#
#         win2 = sg.Window('Window 2').Layout(layout2)
#
#     if win2_active:
#         ev2, vals2 = win2.Read()
#         if ev2 in (None, 'Exit', '< Prev'):
#             win2_active = False
#             win2.Close()
#             win1.UnHide()
#         elif ev2 == 'Next >':
#             win3_active = True
#             win2_active = False
#             win2.Hide()
#             layout3 = [[sg.Text('Window 3')],
#                        [sg.Button('< Prev'), sg.Button('Exit')]]
#             win3 = sg.Window('Window 3').Layout(layout3)
#
#     if win3_active:
#         ev3, vals3 = win3.Read()
#         if ev3 == '< Prev':
#             win3.Close()
#             win3_active = False
#             win2_active = True
#             win2.UnHide()
#         elif ev3 in (None, 'Exit'):
#             break
