from __init__ import *
import login
# import easygui as gui
import PySimpleGUI as sg


# msg = "Welcome to Xpnsit, the best way to manage your expenses! To begin, login or signup below"
# title = 'Xpnsit v0.1'
# login_fields = ['Username','Password']
# gui.Popup(msg,title = title)



window = sg.Window('Xpnsit v0.1')
layout = [
          [sg.Text('Please enter your Name, Address, Phone')],
          [sg.Text('Name', size=(15, 1)), sg.InputText('1', key='_name_')],
          [sg.Text('Address', size=(15, 1)), sg.InputText('2', key='_address_')],
          [sg.Text('Phone', size=(15, 1)), sg.InputText('3', key='_phone_')],
          [sg.Submit(), sg.Cancel(),sg.Button()]
         ]

event, values = window.Layout(layout).Read()

sg.Popup(event, values, values['_name_'], values['_address_'], values['_phone_'])
