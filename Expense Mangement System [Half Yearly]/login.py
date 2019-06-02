################################ Functions for user login and signup etc. ##################################################
import stdiomask
import re
import sys
from __init__ import *
# import errors


login_cursor = conn.cursor()
email_regex = '^[_A-z0-9-]+(\.[_A-z0-9-]+)*@[A-z0-9-]+(\.[A-z0-9-]+)*(\.[A-z]{2,4})$'

class User():
    def user_login(self):

        # def enter_password(): ##Needed to do this so I could kepp the passwords above 8 characters.
        #     return password
        name_cursor = conn.cursor()

        c = True ## Condition for continuing login procedures.
        while c == True:
            self.username = input("Enter username : ")
            self.password = stdiomask.getpass("Enter password: ")


            login_cursor.execute('select username,passwd from users;')
            # print(login_cursor.fetchall())

            if (self.username,self.password) in login_cursor.fetchall():
                name_cursor.execute("select first_name,last_name from users where username = '{}' and passwd = '{}' ;".format(self.username,self.password))
                name = name_cursor.fetchall()
                # print(name)
                print ("Login Success!")
                print("\nWelcome {} {}!".format(name[0][0],name[0][1]))
                c = False

            else:
                print("Username or password incorrect. Please try again!")
                continue_or_not = input('Continue? (y/n)')
                if continue_or_not == 'n':
                    print("Ok! See ya later!")
                    sys.exit()
                elif continue_or_not == 'y':
                    c = True

    def signup(self):

        username_correct = False
        check_cursor = conn.cursor()
        while username_correct == False:

            self.username = input("Enter username: ")
            check_cursor.execute('select username from users;')
            result_set = check_cursor.fetchall()
            # print(result_set)
            for i in result_set:
                if self.username == i[0]:
                    print("Sorry! Username not available")
                    # username_correct = False
                    self.username = input("Enter username: ")
                    # break
                else:
                    username_correct = True
                    break



        password_is_correct = False
        while password_is_correct == False:
            self.password = stdiomask.getpass("Enter password (hidden for security reasons): ")
            # print(password)

            if len(self.password) < 8:
                print("Password less than 8 characters. Try again")
            elif len(self.password) >= 8:
                password_is_correct = True
                break

        T = True
        while(T == True):
            self.email_id = input('Enter email address (Optional, for communication purposes only): ')
            if self.email_id == '':
                self.email_id = 'NULL'
                T = False
                break
            matches = re.match(email_regex,self.email_id)
            if matches == None:
                print('Please input a valid email address.')
            else:
                T = False

        self.first_name = input("Enter first name: ")
        self.last_name = input('Enter last name (surname): ')

        login_cursor.execute("insert into users (username,passwd,email_id,first_name,last_name) values ('{}','{}','{}','{}','{}');".format(self.username,self.password,self.email_id,self.first_name,self.last_name) )
        conn.commit()
    # login_cursor_2 = conn.cursor()
    # login_cursor_2.execute('select username,passwd from users;')
    #
    # for i in login_cursor_2.fetchall():
    #     print(i)
