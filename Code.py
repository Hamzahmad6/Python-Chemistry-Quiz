import tkinter as tk
from tkinter import messagebox
import random
from datetime import datetime

questions = [
    ("What is the molecular formula of water?", ["H2O", "CO2", "CH4", "NaCl"], "H2O"),
    ("What is the pH of a neutral solution?", ["7", "5", "2", "10"], "7"),
    ("What is the chemical symbol for gold?", ["Au", "Ag", "Fe", "Pb"], "Au"),
    ("Which gas is used in photosynthesis?", ["CO2", "O2", "N2", "H2"], "CO2"),
    ("What is the atomic number of oxygen?", ["8", "6", "10", "12"], "8"),
    ("Which acid exists in vinegar?", ["Acetic Acid", "Sulfuric Acid", "Nitric Acid", "Hydrochloric Acid"], "Acetic Acid"),
    ("What is the lightest element?", ["Hydrogen", "Helium", "Carbon", "Nitrogen"], "Hydrogen"),
    ("What is the formula of methane?", ["CH4", "CO2", "C2H6", "H2O"], "CH4"),
    ("Which particle has no charge?", ["Neutron", "Electron", "Proton", "Ion"], "Neutron"),
    ("Which metal is liquid at room temperature?", ["Mercury", "Iron", "Silver", "Copper"], "Mercury"),
    ("What is the unit of amount of substance?", ["Mole", "Gram", "Liter", "Newton"], "Mole"),
    ("Which gas causes global warming most?", ["CO2", "O2", "H2", "N2"], "CO2"),
    ("What is the charge of a proton?", ["+1", "0", "-1", "+2"], "+1"),
    ("What is the symbol of sodium?", ["Na", "So", "S", "Sn"], "Na"),
    ("Which gas is called laughing gas?", ["Nitrous Oxide", "Oxygen", "Carbon Dioxide", "Hydrogen"], "Nitrous Oxide")
]

random.shuffle(questions)

for question in questions:
    random.shuffle(question[1])

root = tk.Tk()
root.title("Advanced Chemistry Exam System")
root.geometry("950x650")
root.configure(bg="#0f172a")
root.resizable(False, False)

current_question = 0
selected_answer = tk.StringVar()
answers = [None] * len(questions)
time_left = 300
student_name = ""
student_age = ""
student_id = ""

def update_timer():
    global time_left
    minutes = time_left // 60
    seconds = time_left % 60
    timer_label.config(text=f"Time Left: {minutes:02}:{seconds:02}")

    if time_left > 0:
        time_left -= 1
        root.after(1000, update_timer)
    else:
        calculate_result()

def load_question():
    global current_question
    question, options, _ = questions[current_question]

    question_label.config(
        text=f"Q{current_question + 1}: {question}"
    )

    progress_label.config(
        text=f"Question {current_question + 1} / {len(questions)}"
    )

    for i, option in enumerate(options):
        option_buttons[i].config(
            text=option,
            value=option
        )

    selected_answer.set(answers[current_question])

def next_question():
    global current_question
    selected = selected_answer.get()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select an answer first!"
        )
        return

    answers[current_question] = selected

    if current_question < len(questions) - 1:
        current_question += 1
        load_question()
    else:
        calculate_result()

def previous_question():
    global current_question

    if current_question > 0:
        current_question -= 1
        load_question()

def calculate_result():
    score = 0

    for i in range(len(questions)):
        _, _, correct_answer = questions[i]
        if answers[i] == correct_answer:
            score += 1

    percentage = (score / len(questions)) * 100

    if percentage >= 90:
        grade = "Excellent"
    elif percentage >= 75:
        grade = "Very Good"
    elif percentage >= 60:
        grade = "Good"
    else:
        grade = "Fail"

    save_result(score, percentage, grade)

    exam_frame.pack_forget()
    result_frame.pack(fill="both", expand=True)

    result_title.config(text="Exam Completed")

    result_info.config(
        text=
        f"Name: {student_name}\n\n"
        f"Age: {student_age}\n\n"
        f"Student ID: {student_id}\n\n"
        f"Score: {score}/{len(questions)}\n\n"
        f"Percentage: {percentage:.1f}%\n\n"
        f"Grade: {grade}"
    )

def save_result(score, percentage, grade):
    with open("results.txt", "a") as file:
        file.write(f"Date: {datetime.now()}\n")
        file.write(f"Name: {student_name}\n")
        file.write(f"Age: {student_age}\n")
        file.write(f"Student ID: {student_id}\n")
        file.write(f"Score: {score}/{len(questions)}\n")
        file.write(f"Percentage: {percentage:.1f}%\n")
        file.write(f"Grade: {grade}\n")
        file.write("-" * 40 + "\n")

def start_exam():
    global student_name, student_age, student_id

    student_name = name_entry.get().strip()
    student_age = age_entry.get().strip()
    student_id = id_entry.get().strip()

    if not student_name or not student_age or not student_id:
        messagebox.showwarning(
            "Missing Data",
            "Please fill all fields!"
        )
        return

    if not student_age.isdigit():
        messagebox.showwarning(
            "Invalid Age",
            "Age must contain numbers only!"
        )
        return

    login_frame.pack_forget()
    exam_frame.pack(fill="both", expand=True)
    load_question()
    update_timer()

def restart_exam():
    root.destroy()

login_frame = tk.Frame(root, bg="#0f172a")
login_frame.pack(fill="both", expand=True)

login_title = tk.Label(
    login_frame,
    text="CHEMISTRY EXAM SYSTEM",
    font=("Helvetica", 28, "bold"),
    fg="#38bdf8",
    bg="#0f172a"
)
login_title.pack(pady=30)

login_subtitle = tk.Label(
    login_frame,
    text="Student Information",
    font=("Verdana", 18),
    fg="white",
    bg="#0f172a"
)
login_subtitle.pack(pady=10)

name_label = tk.Label(
    login_frame,
    text="Full Name",
    font=("Verdana", 14, "bold"),
    fg="white",
    bg="#0f172a"
)
name_label.pack(pady=5)

name_entry = tk.Entry(
    login_frame,
    font=("Verdana", 14),
    width=30,
    justify="center"
)
name_entry.pack(pady=10)

age_label = tk.Label(
    login_frame,
    text="Age",
    font=("Verdana", 14, "bold"),
    fg="white",
    bg="#0f172a"
)
age_label.pack(pady=5)

age_entry = tk.Entry(
    login_frame,
    font=("Verdana", 14),
    width=30,
    justify="center"
)
age_entry.pack(pady=10)

id_label = tk.Label(
    login_frame,
    text="Student ID",
    font=("Verdana", 14, "bold"),
    fg="white",
    bg="#0f172a"
)
id_label.pack(pady=5)

id_entry = tk.Entry(
    login_frame,
    font=("Verdana", 14),
    width=30,
    justify="center"
)
id_entry.pack(pady=10)

start_button = tk.Button(
    login_frame,
    text="Start Exam",
    command=start_exam,
    font=("Helvetica", 15, "bold"),
    bg="#38bdf8",
    fg="black",
    padx=20,
    pady=10,
    cursor="hand2"
)
start_button.pack(pady=30)

exam_frame = tk.Frame(root, bg="#111827")

timer_label = tk.Label(
    exam_frame,
    text="Time Left: 05:00",
    font=("Helvetica", 16, "bold"),
    fg="#f87171",
    bg="#111827"
)
timer_label.pack(pady=15)

progress_label = tk.Label(
    exam_frame,
    text="",
    font=("Verdana", 14, "bold"),
    fg="#38bdf8",
    bg="#111827"
)
progress_label.pack(pady=10)

question_label = tk.Label(
    exam_frame,
    text="",
    font=("Helvetica", 20, "bold"),
    fg="white",
    bg="#111827",
    wraplength=700,
    justify="center"
)
question_label.pack(pady=30)

option_buttons = []

for i in range(4):
    btn = tk.Radiobutton(
        exam_frame,
        text="",
        variable=selected_answer,
        value="",
        font=("Verdana", 14),
        bg="#1e293b",
        fg="white",
        selectcolor="#0ea5e9",
        activebackground="#334155",
        activeforeground="white",
        indicatoron=0,
        width=35,
        pady=12,
        cursor="hand2"
    )

    btn.pack(pady=10)
    option_buttons.append(btn)

nav_frame = tk.Frame(exam_frame, bg="#111827")
nav_frame.pack(pady=30)

prev_button = tk.Button(
    nav_frame,
    text="Previous",
    command=previous_question,
    font=("Helvetica", 13, "bold"),
    bg="#f59e0b",
    fg="white",
    padx=20,
    pady=10,
    cursor="hand2"
)
prev_button.pack(side="left", padx=20)

next_button = tk.Button(
    nav_frame,
    text="Next",
    command=next_question,
    font=("Helvetica", 13, "bold"),
    bg="#22c55e",
    fg="white",
    padx=20,
    pady=10,
    cursor="hand2"
)
next_button.pack(side="right", padx=20)

result_frame = tk.Frame(root, bg="#020617")

result_title = tk.Label(
    result_frame,
    text="",
    font=("Helvetica", 28, "bold"),
    fg="#22c55e",
    bg="#020617"
)
result_title.pack(pady=30)

result_info = tk.Label(
    result_frame,
    text="",
    font=("Verdana", 16),
    fg="white",
    bg="#020617",
    justify="left"
)
result_info.pack(pady=20)

exit_button = tk.Button(
    result_frame,
    text="Exit Program",
    command=root.destroy,
    font=("Helvetica", 14, "bold"),
    bg="#ef4444",
    fg="white",
    padx=20,
    pady=10,
    cursor="hand2"
)
exit_button.pack(pady=20)

restart_button = tk.Button(
    result_frame,
    text="Restart Program",
    command=restart_exam,
    font=("Helvetica", 14, "bold"),
    bg="#3b82f6",
    fg="white",
    padx=20,
    pady=10,
    cursor="hand2"
)
restart_button.pack(pady=10)

root.mainloop()