import sqlite3

# To use the module, you must first create a Connection object that represents the database. 
# Here the data will be stored in the example.db file:
connection = sqlite3.connect("Project1_Quiz_cs384.db")

# Once you have a Connection, you can create a Cursor object and call its execute() 
# method to perform SQL commands:
cursor = connection.cursor()

# basic structure of database
# schema of database
# we have two tables
# one will store the information of registered students
# second will store the score of students in different quizzes


# schema for this table will be name, roll_number, password, whatsapp_num
cursor.execute(
'''
CREATE TABLE IF NOT EXISTS Project1_registration(
name VARCHAR(20) NOT NULL,
roll_number VARCHAR(20) NOT NULL,
password VARCHAR(20) NOT NULL,
whatsapp_num INT NOT NULL);
'''
)

# schema roll number, quiz number, marks in that quiz_num
cursor.execute(
'''
CREATE TABLE IF NOT EXISTS Project1_marks(
roll_num VARCHAR(20) NOT NULL,
quiz_num INT NOT NULL,
total_marks INT NOT NULL);
'''
)

connection.commit()