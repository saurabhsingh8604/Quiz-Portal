import sqlite3
import os
import csv

def exportdb():
    connection = sqlite3.connect("Project1_Quiz_cs384.db")
    entries = connection.execute("SELECT * FROM Project1_marks")
    for entry in entries:
        quiz_num = entry[1]
        rollNo = entry[0]
        marks = entry[2]
        if not os.path.exists(os.getcwd() + "\\quiz_wise_responses\\" + "scores_q" + str(quiz_num) + ".csv"):
            qfile = open(os.getcwd() + "\\quiz_wise_responses\\" + "scores_q" + str(quiz_num) + ".csv","a",newline='')
            fwriter = csv.DictWriter(qfile, ["roll_number","total_marks"])
            fwriter.writeheader()
            fwriter.writerow({"roll_number" : rollNo, "total_marks" : marks})
        else:
            qfile = open(os.getcwd() + "\\quiz_wise_responses\\" + "scores_q" + str(quiz_num) + ".csv","a",newline='')
            fwriter = csv.DictWriter(qfile, ["roll_number","total_marks"])
            fwriter.writerow({"roll_number":rollNo,"total_marks":marks})
    connection.commit()
  
def gotoQuestion(question_list, response):
    quesNum = int(input("Enter the question number you want to go to: "))
    row = question_list[quesNum-1]
    print("Question "+row['ques_no']+") "+row['question'])
    print("Option 1) "+row['option1'])
    print("Option 2) "+row['option2'])
    print("Option 3) "+row['option3'])
    print("Option 4) "+row['option4'])
    print("\n")
    print("Credits if Correct Option: "+row['marks_correct_ans'])
    print("Negative Marking: "+row['marks_wrong_ans'])
    
    if row['compulsory'].lower() == 'y':
        print("Is compulsory: YES")
    else:
        print("Is compulsory: NO")
    
    if len(response) >= quesNum:
        print("Your marked choice is:", response[quesNum-1])
    else:
        print("You have not attempted this question yet")
    print("\n")
    
def showUnattempted(unattempted):
    print("\nUnattempted questions are:",unattempted,"\n")