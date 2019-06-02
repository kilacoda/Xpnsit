from tkinter import *
from tkinter import ttk
from __init__ import *
import login


# print("\nWelcome to the Dashboard. This is where all the functions of Xpnsit lie. Look around and make yourself comfortable!")


class Xpnsit(Tk):
    # def __init__(self, *args, **kwargs):
    #     Tk.__init__(self, *args, **kwargs)
    #
    # def show_frame(self, frame):
    #     frame.tkraise(self)
    def __init__(self):
        tk.Tk.__init__(self)
        self.frame = None
        self.switch_frame(Dashboard)

    def switch_frame(self, frame_class):
        if self.frame is not None:
            self.frame.destroy()
        new_frame = frame_class()
        self.frame = new_frame
        self.frame.pack()


class LoginFrame(Frame):
    def __init__(self, master):
        # super().__init__(master)
        Frame.__init__(self, master)
        master.title('Xpnsit v0.1')
        master.resizable(width = 0, height = 0)
        self.entry_label = Label(self,text = "Welcome to Xpnsit, the best way to manage your expenses! To begin, login or signup below")
        self.label_username = Label(self, text="Username")
        self.label_password = Label(self, text="Password")

        self.entry_username = Entry(self)
        self.entry_password = Entry(self, show="*")

        self.label_username.grid(row=1,column = 1 ,sticky=W)
        self.label_username.grid_columnconfigure(1, weight=150,minsize=200)

        self.label_password.grid(row=2,column = 1, sticky=W)
        self.label_password.grid_columnconfigure(1, weight=150,minsize=200)

        self.entry_username.grid(row=1, column=1)
        self.entry_password.grid(row=2, column=1)
        self.entry_label.grid(row = 0,sticky = NSEW, columnspan = 3)


        """TODO: Create a logout and signup function in the login file, as well as a password reset form and link them to these buttons."""
        self.checkbox = Checkbutton(self, text="Keep me logged in")
        self.checkbox.grid(columnspan=3)

        
        self.logbtn = Button(self, text="Login", command= lambda : [self._login_btn_clicked, Xpnsit.switch_frame(Dashboard)])
        self.logbtn.grid(columnspan=3)

        self.pack()

    def _login_btn_clicked(self):
        # print("Clicked")
        username = self.entry_username.get()
        password = self.entry_password.get()
        message = StringVar()
        status_label = Label(self,textvariable = message)
        status_label.grid(row  = 5, column = 1)

        login.login_cursor.execute('select username,passwd from users;')
        if (username,password) in login.login_cursor.fetchall():
            message.set("Login Success!")
            Xpnsit.switch_frame(self,Dashboard)
            # self.destroy()
            # status_label.config(text = '')
            # status_label.config(text = 'Login Success!')
        else:
            message.set("Username or password incorrect. Please try again!")
            # status_label.config(text = '')
            # status_label.config(text = 'Username or password incorrect. Please try again!')

class Dashboard(Toplevel):
    def __init__(self):
        super().__init__(Toplevel)
        self.title('Dashboard - Xpnsit v0.1')
        self.resizable(True, True)
        self.new_transaction = Button(self, text="New Transaction")
        self.notebook = Button(self, text="Notebook")

        self.analytics = Button(self, text = "Analytics")
        self.transaction_list = Button(self, text = "Transaction List")

        self.new_transaction.grid(row=1,column = 0 ,sticky=NSEW)
        self.new_transaction.grid_columnconfigure(1, weight=1,minsize=200)

        self.notebook.grid(row=2,column = 0, sticky=NSEW)
        self.notebook.grid_columnconfigure(1, weight=1,minsize=200)

        self.analytics.grid(row=3, column=0)
        self.transaction_list.grid(row=4, column=0)

        self.Toplevel.pack()

root = Tk()
login_app = LoginFrame(root)

# dashboard = Toplevel()
# dash_app = Dashboard(dashboard)

root.mainloop()





# get_em_credentials()
# root = Tk()

# top_frame = tkinter.Frame(root).pack()
# bottom_frame = tkinter.Frame(root).pack(side  = 'bottom')


############################Login Entry Spaces#########################################
# def get_em_credentials():







# class App:
#     def __init__(self, master):
#         self.master = master
#         self.success_label = ttk.Label(self.master, text  = '')
#         self.success_label.grid(row  = 3, column = 1)
#
#         # master.geometry('512x800')
#         # master.resizable(width = 0,height = 0)
#
#         self.entry_label.grid(row = 0, column = 0)
#         u_label = ttk.Label(master, text = 'Username: ')
#         u_label.grid(row = 1, column = 0 )
#
#         self.entered_username = ttk.Entry(master)
#         self.entered_username.grid(row = 1, column = 1 )
#
#         p_label = ttk.Label(master, text = 'Password')
#         p_label.grid(row =2 , column = 0)    # l_pass.place(relx = 0.4, rely = 0.4)
#
#         self.entered_password = ttk.Entry(master, show = '*')
#         self.entered_password.grid(row = 2, column = 1)
#
#         submit_button = ttk.Button( master, text = 'Submit', command = self.submit_button_funcs).grid()
#
#
#     def submit_button_funcs(self):
#         self.retrieve_passwords(self.entered_username,self.entered_password)
#         self.success_label.config(text = 'Login Success!')
#
#
#
#     def retrieve_passwords(self,username,password):
#
#         # try:
#         stored_username = username.get()
#         stored_password = password.get()
#         print(stored_username,stored_password)
#
#         # except:
#         #     print("Sorry, I'm a bit stupid and couldn't realize that you hadn't even opened the app. Sorry")
