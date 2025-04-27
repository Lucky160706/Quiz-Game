from question_model import Question
from quiz_brain import QuizBrain
from ui import QuizInterface
import os
from os import listdir
import random

folder_dir = "../New Dataset"
question_data = []
for images_path in os.listdir(folder_dir):
    if (images_path.endswith(".jpg")):
        normalized_path = os.path.normpath(images_path)
        label = images_path.split("_")[0]
        question_data.append(('../New Dataset/' + images_path, label))

question_bank = []
for question in question_data:
    question_text = question[0]  
    question_answer = question[1]  
    new_question = Question(question_text, question_answer)  
    question_bank.append(new_question)


random.shuffle(question_bank)
quiz = QuizBrain(question_bank)
quiz_ui = QuizInterface(quiz)
QuizInterface.start_main_screen()
