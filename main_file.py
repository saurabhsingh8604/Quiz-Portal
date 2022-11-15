import sqlite3
import os
import csv
import time
import threading
import keyboard 
from threading import *
import Login_portal
import Registration_Portal
import Helping_Functions
import Display_Question
import Display_Result
import Create_Tables

global question_list
# SQLite is a C library that provides a lightweight disk-based database that doesn’t require 
# a separate server process and allows accessing the database using a nonstandard variant of 
# the SQL query language. 


# we are storing the quiz_wise response of students in csv files and
# if path to those folders doesn't exist then we'll create 
# same goes for individual response
if not os.path.exists(os.getcwd()+"\\quiz_wise_responses"):
    os.mkdir("quiz_wise_responses")
if not os.path.exists(os.getcwd()+"\\individual_responses"):
    os.mkdir("individual_responses")


# dictonary to has the quiz with integer key
responses = {
            1: "q1",
            2: "q2",
            3: "q3"   
        }

# initial timer
t = -1

# To use the module, you must first create a Connection object that represents the database. 
# Here the data will be stored in the example.db file:
connection = sqlite3.connect("Project1_Quiz_cs384.db")

# Once you have a Connection, you can create a Cursor object and call its execute() 
# method to perform SQL commands:
cursor = connection.cursor()

# to know if user exited the quiz
temp = 0

# timer
def countdown(): 
    global t
    global temp
    while t: 
        mins, secs = divmod(t, 60) 
        timer = '{:02d}:{:02d}'.format(mins, secs) 
        print(timer,"\s", end="\r") 
        time.sleep(1) 
        t -= 1
        # temp == 1 represents that user has exited the quiz
        if temp == 1:
            t = 0
            print('\nYour responses have been saved')
            temp = 0
            return
    print('\nTime Up!! Your responses have been saved \nEnter any valid key to exit')

unattempted = []         
def quiz(info):
    global t
    global question_list
    global unattempted
    global response
    global total_marks_obtained
    global total_marks
    global unattempted_num
    global correct_questions
    global wrong_choices
    global total_questions
    global attempted_questions
    
    print('\n' * 4 + '*' * 25 + 'WELCOME' + '*' * 25)
    quiz_num = input("please choose a quiz which you want to attempt(Please enter quiz number) \n1.Quiz1\n2.Quiz2\n3.Quiz3\n")
    path = os.getcwd() + '\\' + 'quiz_wise_questions'
    curpath = os.getcwd()
    os.chdir(path)
    # path of file that has the questions of quiz_num
    filename = responses[int(quiz_num)] + '.csv'
    f = open(filename, 'r')
    with f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == 'ques_no':
                temp = row[10]
                t = temp[5:-1]
    qfile = open(filename, 'r')
    freader = csv.DictReader(qfile)
    os.chdir(curpath)
    t = 120
    response = []
    correct_questions = 0
    total_marks = 0
    attempted_questions = 0
    total_marks_obtained = 0
    total_questions = 0
    unattempted_num = 10
    wrong_choices = 0
    unattempted = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    question_list = []
    t1 = threading.Thread(target = countdown)
    t1.start()
    for row in freader:
        question_list.append(row)
        total_questions += 1
        
    print('\n' * 4 + '*' * 25 + 'QUIZ STARTS' + '*' * 25)
    
    for row in question_list:
        if t == 0:
            break
        Display_Question.display(row, info, t)
        valid_response = ['1','2','3','4','S','s']
        while True:
            choice = input("\nEnter Choice 1, 2, 3, 4, S(S is to skip question): \n")
            if choice in valid_response:
                break
            else:
                print("please enter valid choice")
        if t == 0:
            break
        #keyboard.add_hotkey("ctrl+alt+U", lambda : print("Unattempted Questions are:",unattempted))
        response.append(choice)
        if choice.lower() == 's':
            if row['compulsory'].lower() == 'y':
                total_marks_obtained += int(row['marks_wrong_ans'])
        else:
            unattempted.remove(int(row['ques_no']))
            attempted_questions += 1
            if row['correct_option'] == choice:
                correct_questions += 1
                total_marks_obtained += int(row['marks_correct_ans'])
            else:
                wrong_choices += 1
                total_marks_obtained += int(row['marks_wrong_ans'])
        print('\n' * 2)
    
    total_marks = 0
    with open(path + '\\' + 'q' + quiz_num + '.csv','r') as file:
        questions = csv.reader(file)
        for question in questions:
            if question[0] == 'ques_no':
                continue
            if int(question[0]) in unattempted and question[9].lower() == 'y':
                total_marks_obtained += int(question[8])
            total_marks += int(question[7])
    with open(path + '\\' + 'q' + quiz_num + '.csv','r') as file:
        questions = csv.reader(file)
        itr = 0
        response = response + ['s'] * (10 - len(response))
        for question in questions:
            with open(os.getcwd() + '\\' + 'individual_responses' + '\\' + 'q' + quiz_num + '_' + info[1] + '.csv', 'a', newline='') as wfile:
                writer = csv.writer(wfile)
                if question[0] == 'ques_no':
                    writer.writerow(question + ['marked_choice','Total','Legend'])
                    continue
                if itr == 0:
                    writer.writerow(question + [response[itr],correct_questions,'Correct Choices'])
                elif itr == 1:
                    writer.writerow(question + [response[itr],wrong_choices,'Wrong Choices'])
                elif itr == 2:
                    writer.writerow(question + [response[itr],len(unattempted),'Unattempted'])
                elif itr == 3:
                    writer.writerow(question + [response[itr],total_marks_obtained,'Marks Obtained'])
                elif itr == 4:
                    writer.writerow(question + [response[itr],total_marks,'Total Quiz Marks'])
                else:
                    writer.writerow(question + [response[itr],'',''])
                itr += 1
    total_quiz_questions = len(response)
    Display_Result.display(total_quiz_questions, correct_questions, attempted_questions, wrong_choices, total_marks_obtained,total_marks)
    t1.join()
    quiz_num = int(quiz_num)
    find_user=("SELECT * FROM Project1_marks WHERE roll_num = ? AND quiz_num = ?")
    cursor.execute(find_user,[(info[1]),(quiz_num)])
    results = cursor.fetchall()
    if results:
        cursor.execute('DELETE FROM Project1_marks WHERE roll_num = ? AND quiz_num = ?',(info[1],quiz_num))
    insertData='''INSERT INTO Project1_marks(roll_num,quiz_num,total_marks)
    VALUES(?,?,?)'''
    cursor.execute(insertData,[(info[1]),(quiz_num),(total_marks_obtained)])
    connection.commit()
    
def multi_quiz(info):
    while True:
        quiz(info)
        res = input("would you like to attempt one more quiz:(Y/N) ")
        if res.lower() != 'y':
            break
    return
    
def final_submit():
    global temp
    x = input('Are you sure you want to submit?(Y/N)')
    if x.lower() == 'y':
        temp = 1

#hotkeys
keyboard.add_hotkey("Ctrl+Alt+G", Helping_Functions.gotoQuestion(question_list , response))

keyboard.add_hotkey("Ctrl+Alt+U", Helping_Functions.showUnattempted(unattempted))

keyboard.add_hotkey("Ctrl+Alt+F", final_submit)

keyboard.add_hotkey("Ctrl+Alt+E", Helping_Functions.exportdb)



# main function
if __name__ == '__main__':
    while True:
        user_choice = input("Do you have an account(y/n)  ")
        if(user_choice.lower() == 'n'):
            Registration_Portal.register()
            break
        elif(user_choice.lower() == 'y'):
            break
        else:
            print("/nplease enter a valid key")
    Login_portal.login()