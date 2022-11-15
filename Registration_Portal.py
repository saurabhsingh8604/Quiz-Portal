# imports
import sqlite3
#local database bn jata hai 

connection = sqlite3.connect("Project1_Quiz_cs384.db")
cursor = connection.cursor()
#cursor us connection se kuch action perfor krne k liye

# if user is not registered
# then they have to register first, only then they will be allowed to attempt quiz
def register():
    found = 0
    #mila y nhi mila 
    print('\n' * 4 + '*' * 25 + 'REGISTRATION PORTAL' + '*' * 25)
    while found == 0:
        roll_number = input("Please enter your roll number: ")
        # query to find the users in database/ user table
        find_user = ("SELECT * FROM Project1_registration WHERE roll_number = ?")
        cursor.execute(find_user,[(roll_number)])
        #array of parameter
        if cursor.fetchall():
            print("Your account already exists please log in")
            return
        else:
            found = 1
    name = input("Please enter your name: ")
    password = input("Please enter your password: ")
    whatsapp_num = input("Please enter your whatsapp number: ")
    insertData = '''INSERT INTO Project1_registration(name,roll_number,password,whatsapp_num)
    VALUES(?,?,?,?)'''
    cursor.execute(insertData, [(name),(roll_number),(password),(whatsapp_num)])
    connection.commit()