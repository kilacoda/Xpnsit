# Goal : To create a working personal expense management system using MySQL and Python
# See README.txt for more project details.
# from tkinter import *
import mysql.connector as mysqlconnect

dbcredentials = {'host': 'localhost',
                 'password': 'bIgnInja349', 'user': 'root'}

conn = mysqlconnect.connect(**dbcredentials)


'''
TODO: Create the database and required tables if they don't exist. This'll be required for systems other than my local one. (Update -> Done)
'''
db_connection_cursor = conn.cursor()


def start_connection():
    # <----------------- Database Creation ----------------------> #
    db_connection_cursor.execute('CREATE DATABASE IF NOT EXISTS xpnsit;')
    db_connection_cursor.execute('USE xpnsit')

    # <----------------- Create Transactions Table ----------------> #
    db_connection_cursor.execute(
        """CREATE TABLE IF NOT EXISTS transactions(
        trans_id int(11) PRIMARY KEY AUTO_INCREMENT,
        user_id int(5) NOT NULL,
        username varchar(35),
        particulars varchar(512),
        exp_type set('CR','DR'),
        amount double,
        exp_date date
    );""")

    # <----------------- Create Users Table ----------------> #
    db_connection_cursor.execute(
        """CREATE TABLE IF NOT EXISTS users(
        user_id int(5) PRIMARY KEY AUTO_INCREMENT,
        username varchar(35),
        passwd varchar(40),
        email_id varchar(45),
        first_name tinytext,
        last_name tinytext
    );""")

# <------------------- OLD SYSTEM OF LOGIN (NOT USED) ----------------------> #

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
