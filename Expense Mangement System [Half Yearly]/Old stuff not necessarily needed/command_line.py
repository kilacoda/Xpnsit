from __init__ import *
from login import *
from classes import *
import sys

print('Welcome to Xpnsit, the best way to manage your expenses! To begin, login or signup below.\n')
    # dashboard()
app = MainApp()
app.login_signup()

print("\nWelcome to Xpnsit! Choose one of the options below to get started. Type 'quit' (all lowercase) to exit the application.")

app.dashboard()
"""
elif choice == '2':
    trans_obj.notebook()
and so on
"""
