## Goal : To create a working personal expense management system using MySQL and Python
## See README.txt for more project details.
# from tkinter import *
import mysql.connector as mysqlconnect

dbcredentials = {'host': 'localhost', 'password': 'bIgnInja349', 'user': 'root', 'database': 'xpnsit'}
conn = mysqlconnect.MySQLConnection(**dbcredentials)


'''
TODO: Create the database and required tables if they don't exist. This'll be required for systems other than my local one. 
'''
# db_connection_cursor = conn.cursor()
# db_connection_cursor.execute('create database if not exists')































# import random
# import getpass
# import re
# import login
# import sys
# import stdiomask
# from tkinter import ttk
# import tkinter



# maindb = mysql.connector.connect(
#     host = 'localhost',
#     user = 'root',
#     passwd = 'bIgnInja349',
#     database = 'xpnsit'
# )
#
# cursor = maindb.cursor()
#
# get_em_credentials()
