from __init__ import *
from tabulate import tabulate
from login import *
import datetime
# import matplotlib

class MainApp:
    """Main class of the app; contains different 'frames' and their functions"""

    def login_signup(self):
        # global count
        count = 1
        # print(count)
        self.l_object = User()
        user_or_not = input('Are you a returning user? (y/n) ')
        while count < 10:
            if user_or_not == 'y':
                self.l_object.user_login()
                break
                # print("Successful login!")

            elif user_or_not == 'n':
                print("Ok! Let's get you signed up then\n")
                # user_id = random .randint(10000,99999)
                self.l_object.signup()
                print('Signup successful!')
                break

            else:
                print('Please enter a valid operator.\n')
                count += 1
                login_signup()
                break
        else:
            print('Maximum no. of operations attempted. Please retart the interface once again')

    # login_signup()

    def dashboard(self):
        u_cursor = conn.cursor()
        u_name = self.l_object.username
        u_cursor.execute(f"select user_id,username from users where username = '{u_name}';")
        result = u_cursor.fetchall()
        trans_obj = Transaction(result[0][0],result[0][1])

        print("1. Manage Transactions")
        print("2. Notebook (Under construction)")
        print("3. Analytics (Under construction)")
        print("4. Transaction History\n")

        choice  = input('')
        print('\n')
        if choice  == '1':
            trans_obj.new_transaction()

        elif choice == '4':
            trans_obj.get_records()
        elif choice == 'quit':
            final_answer = input('Exit? (y/n)')
            if final_answer == 'y':
                print("Ok. Goodbye!")
                sys.exit()
            else:
                pass
        self.dashboard()


class Transaction():
    t_cursor = conn.cursor()

    # args = ['name','exp_type','amount','date']
    def __init__(self,user_id,username):

        self.user_id = user_id
        self.username = username

        # self.currency = currency

    def new_transaction(self,*args):

        self.particulars = input('Enter transaction name/particulars: ')
        self.amount =  float(input('Enter transaction amount: ') )
        self.type = input("Income (type CR) or Expenditure (type DR)? ")
        date = input("Date of transaction (dd-mm-yyyy, with dashes): ")

        dated_date = datetime.datetime.strptime(date, '%d-%m-%Y')
        todays_date = datetime.date.today()

        # print(dated_date)
        # print(todays_date)
        while dated_date.date() > todays_date :

            print("Please enter a valid date from before today or today\n")
            date = input("Date of transaction (dd-mm-yyyy, with dashes): ")


        self.newdate = date[-4:] + '-' + date[3:5] + '-' + date[0:2]
        finality = input("\nConfirm operation? (y/n)")
        if finality == 'y':
            self.t_cursor.execute(f"insert into transactions values('{self.user_id}','{self.username}','{self.particulars}','{self.type}','{self.amount}','{self.newdate}')")
            conn.commit()
            print("Operation successful!")
        else:
            print("Okay. Operation aborted.")

    def get_records(self):
        print("Sort according to? (enter corresponding value)" + '\n')
        print("""1. Name
2. Date
3. Amount
4. Type (CR/DR)""" + '\n')

        val_dict = {'1':'username',
                    '2':'exp_date',
                    '3':'amount',
                    '4':'exp_type' }


        choice = input('')
        if choice != '':
            self.sort_choice = val_dict[choice]

            self.t_cursor.execute(f"select particulars,exp_type,amount,exp_date from transactions where user_id = {self.user_id} order by {self.sort_choice};")

        elif choice == '3':
            choice_2  = input("Ascending (a) or Descending (d)?")
            if choice_2 == 'a':
                self.t_cursor.execute(f"select particulars,exp_type,amount,exp_date from transactions where user_id = {self.user_id} order by amount asc;")
            else:
                self.t_cursor.execute(f"select particulars,exp_type,amount,exp_date from transactions where user_id = {self.user_id} order by amount desc;")


        else:
            self.t_cursor.execute(f"select particulars,exp_type,amount,exp_date from transactions where user_id = {self.user_id};")

        print(tabulate(self.t_cursor.fetchall(), headers = ('Particulars','Type','Amount','Date'), tablefmt="fancy_grid") + '\n')

    # def analysis(self):
