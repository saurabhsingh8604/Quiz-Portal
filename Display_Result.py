def display(total_quiz_questions, correct_questions, attempted_questions, wrong_choices, total_marks_obtained,total_marks):
  print('''Total Quiz Questions:{}
          Total Quiz Questions Attempted:{}
          Total Correct Question:{}
          Total Wrong Questions:{}
          Total Marks: {}/{}'''
          .format(total_quiz_questions,attempted_questions,correct_questions,wrong_choices,total_marks_obtained,total_marks))
  print("Press Ctrl+Alt+U to see the unattempted questions")
  print("Press Ctrl+Alt+G to go to your desired question")
  print("Press Ctrl+Alt+F to submit the quiz finally")
  print("Press Ctrl+Alt+E to export the database to csv")