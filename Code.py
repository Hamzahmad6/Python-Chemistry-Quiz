import tkinter as tk
from tkinter import messagebox
import random

# Questions data (Question, Options, Correct Answer)
questions = [
    ("What is the molecular formula of water?", ["H2O", "H2O2", "CO2", "CH4"], "H2O"),
    ("What is the main component of table salt?", ["NaCl", "KCl", "CaCO3", "MgCl2"], "NaCl"),
    ("What is the pH of a neutral solution?", ["7", "5", "3", "9"], "7"),
    ("What is the functional group in alcohols?", ["-OH", "-COOH", "-NH2", "-CH3"], "-OH"),
    ("What is the molecular formula of glucose?", ["C6H12O6", "C12H22O11", "C2H5OH", "CH4"], "C6H12O6"),
    ("What is the main gas responsible for global warming?", ["CO2", "O2", "N2", "CH4"], "CO2"),
    ("What is the catalyst used in the Haber process?", ["Fe", "Ni", "Pt", "Cu"], "Fe"),
    ("What is the state of iodine at room temperature?", ["Solid", "Liquid", "Gas", "Plasma"], "Solid"),
    ("What is the charge on a proton?", ["+1", "-1", "0", "+2"], "+1"),
    ("What is the unit of the amount of substance?", ["Mole", "Gram", "Litre", "Kilogram"], "Mole"),
]

# Shuffle questions and options
random.shuffle(questions)
for question in questions:
    random.shuffle(question[1])

# Initialize the main window
root = tk.Tk()
root.geometry("600x400")
root.title("Chemistry Quiz")
root.update_idletasks()  # Ensure window size is accurate
x = (root.winfo_screenwidth() - root.winfo_width()) // 2
y = (root.winfo_screenheight() - root.winfo_height()) // 2
root.geometry(f"+{x}+{y}")
# Global variables
current_question = 0
selected_answer = tk.StringVar()  # Variable to store the selected answer
score = 0  # Initialize score
user_name = ""  # Variable to store the user's name
answers = [None] * len(questions)  # To store user's answers

# Function to load a question
def load_question():
    global current_question

    # Get the current question
    question, options, _ = questions[current_question]

    # Update question label
    question_label.config(text=f"Q{current_question + 1}: {question}")

    # Update the options
    for i, option in enumerate(options):
        option_buttons[i].config(text=option, value=option)
    
    # Set the selected answer if already answered
    selected_answer.set(answers[current_question])

    # Update navigation buttons
    if current_question == 0:
        prev_button.pack_forget()
    else:
        prev_button.pack(side=tk.LEFT, padx=10)

# Function to handle the "Next" button
def next_question():
    global current_question, score

    selected = selected_answer.get()
    
    # Check if no option is selected
    if not selected:  
        messagebox.showwarning("Warning", "You must select an answer before proceeding!")
        return

    # Store the answer
    answers[current_question] = selected

    # Check if the answer is correct
    _, _, correct_answer = questions[current_question]
    if selected == correct_answer:
        score += 1  # Increment score for correct answer

    # Move to the next question
    if current_question < len(questions) - 1:
        current_question += 1
        load_question()  # Load the next question
    else:
        # Show final score
        messagebox.showinfo("Quiz Completed", f"{user_name}, you have completed the quiz! Your score: {score}/{len(questions)}")
        root.quit()  # Exit the application

# Function to handle the "Previous" button
def previous_question():
    global current_question

    # Move to the previous question
    if current_question > 0:
        current_question -= 1
        load_question()  # Load the previous question

# Function to handle the "Start Exam" button
def start_exam():
    global user_name
    user_name = name_entry.get().strip()
    if not user_name:  # Check if the name entry is empty
        messagebox.showwarning("Warning", "You must enter your name to start the exam!")
        return
    
    start_button.pack_forget()  # Hide the start button
    name_label.pack_forget()  # Hide the name label
    name_entry.pack_forget()  # Hide the name entry
    
    question_label.pack(pady=20)  # Show the question label
    for btn in option_buttons:
        btn.pack(anchor="w", padx=100)  # Show the option buttons
    nav_frame.pack(pady=20)  # Show the navigation buttons
    load_question()  # Load the first question

# UI Components
name_label = tk.Label(root, text="Enter your name:", font=("Arial", 12))
name_label.pack(pady=20)

name_entry = tk.Entry(root, font=("Arial", 12))
name_entry.pack(pady=5)

start_button = tk.Button(root, text="Start Exam", command=start_exam, font=("Arial", 12))
start_button.pack(pady=20)

question_label = tk.Label(root, text="", font=("Arial", 14), wraplength=400, justify="center")
# Initially not packing the question_label

# Radio buttons for options
option_buttons = []
for i in range(4):  # 4 options per question
    btn = tk.Radiobutton(root, text="", variable=selected_answer, font=("Arial", 12), value="")
    option_buttons.append(btn)
    # Initially not packing the option buttons

# Navigation frame for Next and Previous buttons
nav_frame = tk.Frame(root)
prev_button = tk.Button(nav_frame, text="Previous", command=previous_question, font=("Arial", 12))
next_button = tk.Button(nav_frame, text="Next", command=next_question, font=("Arial", 12))
next_button.pack(side=tk.RIGHT, padx=10)
# Initially not packing the nav_frame

# Run the application
root.mainloop()
