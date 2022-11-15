# imports
import sqlite3
import Helping_Functions

connection = sqlite3.connect("Project1_Quiz_cs384.db")
cursor = connection.cursor()


def login():
    while True:
        print('\n' * 4 + '*' * 25 + 'LOGIN PORTAL' + '*' * 25)
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")
        find_user = ("SELECT * FROM Project1_registration WHERE roll_number = ? AND password = ?")
        cursor.execute(find_user,[(username),(password)])
        # To retrieve data after executing a SELECT statement, you can either treat the cursor as an
        # iterator, call the cursor’s fetchone() method to retrieve a single matching row, or call 
        # fetchall() to get a list of the matching rows.
        results = cursor.fetchall()
        if results:
            for score_detail in results:
                  Helping_Functions.multi_quiz([score_detail[0], score_detail[1], score_detail[2], score_detail[3]])
                  return
        else:
            print("username or password incorrect,try again")
