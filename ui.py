from tkinter import *
from tkinter import messagebox
from quiz_brain import QuizBrain
from question_model import Question
import os
from os import listdir
from PIL import Image, ImageTk
import json
from random import *

# SIGHTENGINE_USER = '14331906'
SIGHTENGINE_USER = "740023025"
# SIGHTENGINE_SECRET = 'Kb9wb6aLjR4wzne3vD8bwbVXhMAEsgXN'
SIGHTENGINE_SECRET = "qhFmfxyvKCM6nFYV3gj7UCET7BnGqqq3"
SIGHTENGINE_API_URL = 'https://api.sightengine.com/1.0/check.json'
AI_MODEL = 'genai'
THEME_COLOR = '#EECEB3'


# ai_image_detect.py
import requests
import secrets

def detect_ai_generated(image_path):
    """
    Calls the Sightengine API to detect if an image is AI-generated.

    Args:
        image_path (str): The full path to the image file.

    Returns:
        float or None: The confidence score for the 'ai_generated' type,
                       or None if there's an error.
    """
    try:
        with open(image_path, 'rb') as image_file:
            files = {'media': (image_path.split('/')[-1], image_file)}
            data = {
                'models': secrets.AI_MODEL,
                'api_user': secrets.SIGHTENGINE_USER,
                'api_secret': secrets.SIGHTENGINE_SECRET
            }
            response = requests.post(secrets.SIGHTENGINE_API_URL, files=files, data=data)
            response.raise_for_status()  # Raise an exception for bad status codes
            json_response = response.json()
            if 'type' in json_response and 'ai_generated' in json_response['type']:
                return json_response['type']['ai_generated']
            else:
                print(f"Warning: 'ai_generated' field not found in the response: {json_response}")
                return None
    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error calling the Sightengine API: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

folder_dir = "../New Dataset"
question_data = []
for images_path in os.listdir(folder_dir):
    if (images_path.endswith(".jpg")):
        normalized_path = os.path.normpath(images_path)
        label = images_path.split("_")[0]
        question_data.append(('../New Dataset/' + images_path, label))
class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain):   
        self.done = False     
        self.quiz = quiz_brain
        self.current_path = None
        self.ai_score_label = None    
        self.window = Tk()
        self.window.title("Quiz App")
        self.window.geometry("500x700")
        self.window.config(bg=THEME_COLOR)
        self.window.resizable(0,0)
        self.game_frame = Frame(bg=THEME_COLOR)
        self.live = 3
        self.high_score = 0

        button_path = "./button/Screenshot 2025-04-27 at 9.40.30 AM.png"
        button_image = Image.open(button_path)
        button_image = button_image.resize((150,54))
        self.button_photo = ImageTk.PhotoImage(button_image)

        self.image1 = PhotoImage(file = "./Adobe Express - file-Picsart-BackgroundRemover.png")
        self.labelimage = Label(
            self.game_frame,
            image = self.image1,
            background=THEME_COLOR,
        )

        self.user_label = Label(
            self.game_frame, 
            text='Username',
            fg="black",
            bg=THEME_COLOR,
            font=('Arial', 20)
        )
        self.password_label = Label(
            self.game_frame, 
            text = "Password",
            fg='black', 
            background=THEME_COLOR,
            font=('Arial', 20)
            )
        self.user_name = Entry(
            self.game_frame, 
            width  = 25,
            background='white', 
            fg = 'black',
            bg='white',
            insertbackground='black',
            highlightthickness=0,
            bd=0
            )
        self.password = Entry(
            self.game_frame, 
            width = 25, 
            background='white',
            fg = 'black',
            bg='white',
            insertbackground='black',
            highlightthickness=0,
            bd=0)
        
        self.button_start = Button(
            self.game_frame,
            bg=THEME_COLOR,
            image=self.button_photo,
            highlightthickness=0,
            command=self.startIspressed,
            bd = 0,
            activebackground=THEME_COLOR,
            cursor='hand2'
        )
        self.generate_password = Button(
            self.game_frame, 
            width = 10, 
            background='white',
            fg = 'black',
            bg='white',
            highlightthickness=0,
            bd=0,
            text="Generate Password", 
            command = self.create_password)
    
        self.game_frame.pack()

        self.labelimage.grid(row=0, column=0, columnspan=3, pady=(10, 20))

        self.user_label.grid(row=1, column=0, pady=(0, 10), sticky='e')
        self.user_name.grid(row=1, column=1, columnspan=2, pady=(0, 10), sticky='we')  

        self.password_label.grid(row=2, column=0, pady=(0, 10), sticky='e')
        self.password.grid(row=2, column=1, pady=(0, 10), sticky='we')
        self.generate_password.grid(row=2, column=2, pady=(0, 10), sticky='w')

        self.button_start.grid(row=3, column=0, columnspan=3, pady=20)

        self.game_frame.columnconfigure(1, weight=1)
        self.game_frame.columnconfigure(2, weight=1)
              
        self.ai_score_label = None
        self.correct_label = None
        self.incorrect_label = None
        
        self.window.mainloop()
    def start_main_screen(self):
        self.window = Tk()
        self.window.title("Quiz App")
        self.window.geometry("500x700")
        self.window.config(bg=THEME_COLOR)
        self.window.resizable(0,0)
        self.game_frame = Frame(bg=THEME_COLOR)
        self.live = 3

        button_path = "./button/Screenshot 2025-04-27 at 9.40.30 AM.png"
        button_image = Image.open(button_path)
        button_image = button_image.resize((150,54))
        self.button_photo = ImageTk.PhotoImage(button_image)

        self.image1 = PhotoImage(file = "./Adobe Express - file-Picsart-BackgroundRemover.png")
        self.labelimage = Label(
            self.game_frame,
            image = self.image1,
            background=THEME_COLOR,
        )

        self.user_label = Label(
            self.game_frame, 
            text='Username',
            fg="black",
            bg=THEME_COLOR,
            font=('Arial', 20)
        )
        self.password_label = Label(
            self.game_frame, 
            text = "Password",
            fg='black', 
            background=THEME_COLOR,
            font=('Arial', 20)
            )
        self.user_name = Entry(
            self.game_frame, 
            width  = 25,
            background='white', 
            fg = 'black',
            bg='white',
            insertbackground='black',
            highlightthickness=0,
            bd=0
            )
        self.password = Entry(
            self.game_frame, 
            width = 25, 
            background='white',
            fg = 'black',
            bg='white',
            insertbackground='black',
            highlightthickness=0,
            bd=0)
        
        self.button_start = Button(
            self.game_frame,
            bg=THEME_COLOR,
            image=self.button_photo,
            highlightthickness=0,
            command=self.startIspressed,
            bd = 0,
            activebackground=THEME_COLOR,
            cursor='hand2'
        )
        self.generate_password = Button(
            self.game_frame, 
            width = 10, 
            background='white',
            fg = 'black',
            bg='white',
            highlightthickness=0,
            bd=0,
            text="Generate Password", 
            command = self.create_password)
    
        self.game_frame.pack()

        self.labelimage.grid(row=0, column=0, columnspan=3, pady=(10, 20))

        self.user_label.grid(row=1, column=0, pady=(0, 10), sticky='e')
        self.user_name.grid(row=1, column=1, columnspan=2, pady=(0, 10), sticky='we')  

        self.password_label.grid(row=2, column=0, pady=(0, 10), sticky='e')
        self.password.grid(row=2, column=1, pady=(0, 10), sticky='we')
        self.generate_password.grid(row=2, column=2, pady=(0, 10), sticky='w')

        self.button_start.grid(row=3, column=0, columnspan=3, pady=20)

        self.game_frame.columnconfigure(1, weight=1)
        self.game_frame.columnconfigure(2, weight=1)
              
        self.ai_score_label = None
        self.correct_label = None
        self.incorrect_label = None
        
        self.window.mainloop()
    
    def create_password(self):
        if self.password:
            self.password.delete(0, END)
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
                'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                'Y', 'Z']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

        password_part1 = [choice(letters) for _ in range(randint(8, 10))]
        password_part2 = [choice(symbols) for _ in range(randint(2, 4))]
        password_part3 = [choice(numbers) for _ in range(randint(2, 4))]
        password_list = password_part1 + password_part2 + password_part3

        shuffle(password_list)
        final_password = "".join(password_list)
        self.password.insert(0, final_password)
        
    def save_data(self):
        user_name = self.user_name.get()
        password = self.password.get()

        new_data = {
            user_name: {
                "password": password,
            }
        }

        if len(user_name) == 0 or len(password) == 0:
            messagebox.showwarning(title="Oops", message="Please don't leave any fields empty!")
        else:
            is_ok = messagebox.askokcancel(
                title=user_name, 
                message=f"These are the details entered:\nUsername: {user_name}\nPassword: {password}\nIs it ok to save?"
            )
            if is_ok:
                try:
                    with open("data.json", "r") as data_file:
                        try:
                            # Attempt to load existing data
                            data = json.load(data_file)
                        except json.decoder.JSONDecodeError:
                            # File exists but is empty or invalid
                            data = {}
                except FileNotFoundError:
                    # File does not exist
                    data = {}

                # Update data with new entry
                data.update(new_data)

                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)

                # Clear the fields after saving
                self.user_name.delete(0, END)
                self.password.delete(0, END)
                self.done = True


    def startIspressed(self):
        self.save_data()
        if self.done:
            self.labelimage.destroy()
            self.user_label.destroy()
            self.password.destroy()
            self.user_name.destroy()
            self.password_label.destroy()
            self.generate_password.destroy()

            self.button_start.destroy()
            self.start_game()
    
    def start_game(self):
        self.game_frame.pack(pady=20)

        self.question_text = Label(
            self.game_frame,
            justify='center',
            text="Was this photo created by AI?",
            fg='black',
            bg=THEME_COLOR,
            font=('Arial', 30, 'italic'),
            wraplength=600  
        )
        self.question_text.grid(row=0, column=0, columnspan=2, pady=20)

        self.canvas = Canvas(self.game_frame, width=300, height=250, bg="white")
        self.image_on_canvas = self.canvas.create_image(150, 125, image=None)
        self.canvas.grid(row=1, column=0, columnspan=2, pady=20)

        self.true_image = PhotoImage(file="images/true.png")
        self.false_image = PhotoImage(file="images/false.png")

        button_frame = Frame(self.game_frame, bg=THEME_COLOR)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(10, 20))

        self.true_button = Button(button_frame, 
                                image=self.true_image, 
                                highlightthickness=0, 
                                command=self.true_pressed,
                                bg=THEME_COLOR,
                                activebackground=THEME_COLOR,
                                bd=0)
        self.true_button.pack(side='left', padx=20)

        self.false_button = Button(button_frame, 
                                image=self.false_image, 
                                highlightthickness=0, 
                                command=self.false_pressed,
                                bg=THEME_COLOR,
                                activebackground=THEME_COLOR,
                                bd=0)
        self.false_button.pack(side='right', padx=20)

        self.score_label = Label(
            self.game_frame, 
            text="Score: 0", 
            fg="black", 
            bg=THEME_COLOR, 
            font=('Arial', 30, 'italic')
        )
        self.score_label.grid(
            row=3, column=0, columnspan=2, 
            pady=5, sticky="n"
            )

        self.get_next_question()
       

    def get_next_question(self):
        self.window.config(bg=THEME_COLOR)
        self.score_label.config(bg=THEME_COLOR)
        self.game_frame.config(bg = THEME_COLOR)
        self.question_text.config(bg=THEME_COLOR)
        self.score_label.config(text=f"Score: {self.quiz.score}     Attempts left: {self.live}")
        if self.incorrect_label:
            self.incorrect_label.destroy()
            self.incorrect_label = None  

        if self.correct_label:
            self.correct_label.destroy()
            self.correct_label = None  
        
        if self.ai_score_label:
            self.ai_score_label.destroy()
    
        if self.quiz.still_has_questions() and self.live > 0:
            question = self.quiz.next_question()  
            q_image_path = question.image_path
            self.current_path = q_image_path
            img = Image.open(q_image_path)
            img = img.resize((300, 250))
            self.current_image = ImageTk.PhotoImage(img)
            self.canvas.itemconfig(self.image_on_canvas, image=self.current_image)

        else:
            # self.canvas.itemconfig(self.image_on_canvas, image='')
            # self.canvas.create_text(
            #     150, 125,
            #     text=f"You've reached the end!\nFinal score: {self.quiz.score}/{self.quiz.question_number}",
            #     fill=THEME_COLOR,
            #     font=("Arial", 16, "italic")
            # )
            # self.true_button.config(state="disabled")
            # self.false_button.config(state="disabled")
            self.game_over()

    def true_pressed(self):
        self.give_feedback(self.quiz.check_answer("Fake"))

    def false_pressed(self):
        is_right = self.quiz.check_answer("Real")
        self.give_feedback(is_right)
    
    def game_over(self):
        self.game_frame.destroy()
        
        # Tạo frame chính cho màn hình Game Over
        self.game_over_screen = Frame(self.window, bg=THEME_COLOR)
        self.game_over_screen.place(relwidth=1, relheight=1)
        
        # Tạo frame con để chứa nội dung (giúp căn giữa dễ dàng hơn)
        content_frame = Frame(self.game_over_screen, bg=THEME_COLOR)
        content_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Tiêu đề GAME OVER
        self.label_game_over = Label(
            content_frame,
            text="GAME OVER", 
            font=("Arial", 40, "bold"),
            bg=THEME_COLOR,
            fg="#D23369"  # Màu đỏ nhạt cho tiêu đề
        )
        self.label_game_over.pack(pady=(0, 30))
        
        # Hiển thị điểm
        self.label_score = Label(
            content_frame,
            text=f"Your Score: {self.quiz.score}",  
            font=("Arial", 24),
            bg=THEME_COLOR,
            fg="black"
        )
        self.label_score.pack(pady=(0, 20))
        
        # Hiển thị high score
        if self.quiz.score <= self.high_score:
            high_score_text = f"High Score: {self.high_score}"
            high_score_color = "black"
        else: 
            self.high_score = self.quiz.score  # Cập nhật high score mới
            high_score_text = "NEW HIGH SCORE!!!"
            high_score_color = "#D23369"  # Màu đỏ nhạt cho high score mới
        
        self.label_high_score = Label(
            content_frame,
            text=high_score_text, 
            font=("Arial", 22, "bold"),
            bg=THEME_COLOR,
            fg=high_score_color
        )
        self.label_high_score.pack(pady=(0, 40))
        
        # Nút/nhãn khởi động lại
        restart_frame = Frame(content_frame, bg=THEME_COLOR)
        restart_frame.pack()
        
        # Sử dụng hình ảnh làm nút (nếu muốn)
        # self.restart_image = PhotoImage(file="./button/restart_button.png")  # Thay bằng đường dẫn ảnh của bạn
        # self.label_restart = Label(
        #     restart_frame,
        #     image=self.restart_image,
        #     bg=THEME_COLOR,
        #     cursor="hand2"
        # )
        # self.label_restart.pack()
        # self.label_restart.bind("<Button-1>", lambda e: self.restart_game())
        
       
        self.label_restart = Label(
            restart_frame,
            text="Click here or press any key to play again",
            font=("Arial", 14),
            bg=THEME_COLOR,
            fg="#555555",
            cursor="hand2"
        )
        self.label_restart.pack()
        # self.label_restart.bind("<Button-1>", lambda e: self.restart_game())
        
        
        # Bind phím bất kỳ để chơi lại
        self.window.bind("<Key>", lambda e: self.restart_game())

# def restart_game(self):
#     """Khởi động lại game"""
#     # Xóa màn hình game over
#     self.game_over_screen.destroy()
#     # Reset các giá trị
#     self.live = 3
#     self.quiz.score = 0
#     self.quiz.question_number = 0
#     # Bắt đầu game mới
#     self.start_game()


    def give_feedback(self, is_right):
        if is_right:
            if self.incorrect_label:
                self.incorrect_label.destroy()  
            image_file_path = self.current_path
            ai_score = detect_ai_generated(image_file_path)
            
            self.correct_label = Label(
                self.game_frame,
                text="Correct",
                fg="green",
                bg=THEME_COLOR,
                font=('Arial', 30, 'bold')
            )
            self.correct_label.grid(row=4, column=0, columnspan=2, pady=(0, 0))

            # self.ai_score_label = Label(
            #     self.game_frame,
            #     text=f"AI generation percentage: {round(ai_score * 100, 2)}%",
            #     fg="black",
            #     bg=THEME_COLOR,
            #     font=('Arial', 25),
            #     wraplength=500,
            #     justify='center'
            # )
            # self.ai_score_label.grid(row=5, column=0, columnspan=4, pady=(5, 0))

          
        else:
            if self.incorrect_label:
                self.incorrect_label.destroy()  # Ensure the label is destroyed before using it again
            # self.window.update()
            # self.game_frame.pack(pady=20)

            image_file_path = self.current_path
            ai_score = detect_ai_generated(image_file_path)
            
            self.incorrect_label = Label(
                self.game_frame,
                text="Incorrect",
                fg="red",
                bg=THEME_COLOR,
                font=('Arial', 30, 'bold')
            )
            self.incorrect_label.grid(row=4, column=0, columnspan=2, pady=(0, 0))

            # print(ai_score)

            # self.ai_score_label = Label(
            #     self.game_frame,
            #     text=f"AI generation percentage: {round(ai_score * 100, 2)}%",
            #     fg="black",
            #     bg=THEME_COLOR,
            #     font=('Arial', 25),
            #     wraplength=500,
            #     justify='center',
            # )
            # self.ai_score_label.grid(row=5, column=0, columnspan=4, pady=(5, 0))
            self.live -= 1
            
        self.window.after(1800, self.get_next_question)

