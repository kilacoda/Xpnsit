import tkinter
from tkinter import messagebox
appWindow = tkinter.Tk()

appWindow.title("Hi, what's up?")

def left_click(event):
    tkinter.Label(appWindow, text = "Left Click!").pack()

def middle_click(event):
    tkinter.Label(appWindow, text = "Middle Click!").pack()

def right_click(event):
    tkinter.Label(appWindow, text = "Right Click!").pack()

appWindow.bind("<Button-1>", left_click)
appWindow.bind("<Button-2>", middle_click)
appWindow.bind("<Button-3>", right_click)


# def hello_world(any_event):
#     tkinter.Label(appWindow,text = 'Hello World!!').pack()
# button = tkinter.Button(appWindow,text='Click me')
# button.bind('<Button-1>',hello_world)
# button.pack()
tkinter.Label(appWindow, text = 'Username').grid(row=0, column = 0)
tkinter.Entry(appWindow).grid(row = 0, column = 1)

tkinter.Label(appWindow, text = 'Password').grid(row=1, column = 0)
tkinter.Entry(appWindow).grid(row = 1, column = 1)
#
# tkinter.Checkbutton(appWindow,text = 'Keep me signed in').grid(columnspan = 2, rowspan = 4)
# ########Frames##################
# top_frame = tkinter.Frame(appWindow).pack()
# bottom_frame = tkinter.Frame(appWindow).pack(side = 'bottom')
#
# #########Buttons###########
# button1 = tkinter.Button(top_frame,text = 'Click me', fg = 'blue', bg = 'yellow').pack()
# button2 = tkinter.Button(top_frame,text = 'Stop it', fg = 'brown', bg = 'green').pack()
# button3 = tkinter.Button(bottom_frame,text = 'Please', fg = 'black', bg = 'purple').pack(fill = 'y')
# button4 = tkinter.Button(bottom_frame,text = 'Ok, I quit.', fg = 'yellow', bg = 'red').pack(side = 'right')
tkinter.messagebox.askquestion("Simple Question","You're dumb")
appWindow.mainloop()
