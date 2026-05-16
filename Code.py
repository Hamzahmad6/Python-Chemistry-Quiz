# Import tkinter for GUI creation
import tkinter as tk

# Import messagebox for popup messages
from tkinter import messagebox

# Import random for shuffling questions
import random

# Import datetime for saving exam date and time
from datetime import datetime


# =========================
# QUESTIONS DATABASE
# =========================

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


# Shuffle questions
random.shuffle(questions)

# Shuffle answers inside each question
for question in questions:
    random.shuffle(question[1])


# =========================
# MAIN WINDOW
# =========================

# Create main window
root = tk.Tk()

# Set title
root.title("Advanced Chemistry Exam System")

# Set size
root.geometry("950x650")

# Set background color
root.configure(bg="#0f172a")

# Disable resizing
root.resizable(False, False)


# =========================
# GLOBAL VARIABLES
# =========================

# Store current question number
current_question = 0

# Store selected answer
selected_answer = tk.StringVar()

# Store all answers
answers = [None] * len(questions)

# Store timer seconds
time_left = 300

# Store student data
student_name = ""
student_age = ""
student_id = ""


# =========================
# FUNCTIONS
# =========================

# Function for countdown timer
def update_timer():

    # Access global variable
    global time_left

    # Calculate minutes
    minutes = time_left // 60

    # Calculate seconds
    seconds = time_left % 60

    # Update timer label
    timer_label.config(text=f"Time Left: {minutes:02}:{seconds:02}")

    # Continue countdown if time remains
    if time_left > 0:

        # Reduce time by one second
        time_left -= 1

        # Call function every second
        root.after(1000, update_timer)

    else:

        # End exam automatically
        calculate_result()


# Function for loading questions
def load_question():

    # Access current question variable
    global current_question

    # Get question data
    question, options, _ = questions[current_question]

    # Display question
    question_label.config(
        text=f"Q{current_question + 1}: {question}"
    )

    # Display progress
    progress_label.config(
        text=f"Question {current_question + 1} / {len(questions)}"
    )

    # Update answer buttons
    for i, option in enumerate(options):

        # Configure answer button
        option_buttons[i].config(
            text=option,
            value=option
        )

    # Restore previous answer if exists
    selected_answer.set(answers[current_question])


# Function for next question
def next_question():

    # Access current question variable
    global current_question

    # Get selected answer
    selected = selected_answer.get()

    # Prevent empty answers
    if not selected:

        # Show warning
        messagebox.showwarning(
            "Warning",
            "Please select an answer first!"
        )

        return

    # Save answer
    answers[current_question] = selected

    # Move to next question if possible
    if current_question < len(questions) - 1:

        # Increase question index
        current_question += 1

        # Load next question
        load_question()

    else:

        # Finish exam
        calculate_result()


# Function for previous question
def previous_question():

    # Access current question variable
    global current_question

    # Check if not first question
    if current_question > 0:

        # Decrease question index
        current_question -= 1

        # Reload question
        load_question()


# Function for calculating result
def calculate_result():

    # Initialize score
    score = 0

    # Loop through all questions
    for i in range(len(questions)):

        # Get correct answer
        _, _, correct_answer = questions[i]

        # Check answer correctness
        if answers[i] == correct_answer:

            # Increase score
            score += 1

    # Calculate percentage
    percentage = (score / len(questions)) * 100

    # Determine grade
    if percentage >= 90:
        grade = "Excellent"
    elif percentage >= 75:
        grade = "Very Good"
    elif percentage >= 60:
        grade = "Good"
    else:
        grade = "Fail"

    # Save result into file
    save_result(score, percentage, grade)

    # Hide exam frame
    exam_frame.pack_forget()

    # Display results frame
    result_frame.pack(fill="both", expand=True)

    # Update result labels
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


# Function for saving results
# Saves results inside results.txt file

def save_result(score, percentage, grade):

    # Open file in append mode
    with open("results.txt", "a") as file:

        # Write exam date
        file.write(f"Date: {datetime.now()}\n")

        # Write student name
        file.write(f"Name: {student_name}\n")

        # Write student age
        file.write(f"Age: {student_age}\n")

        # Write student ID
        file.write(f"Student ID: {student_id}\n")

        # Write score
        file.write(f"Score: {score}/{len(questions)}\n")

        # Write percentage
        file.write(f"Percentage: {percentage:.1f}%\n")

        # Write grade
        file.write(f"Grade: {grade}\n")

        # Add separator line
        file.write("-" * 40 + "\n")


# Function for starting exam

def start_exam():

    # Access global variables
    global student_name
    global student_age
    global student_id

    # Get entered values
    student_name = name_entry.get().strip()
    student_age = age_entry.get().strip()
    student_id = id_entry.get().strip()

    # Validate fields
    if not student_name or not student_age or not student_id:

        # Show warning
        messagebox.showwarning(
            "Missing Data",
            "Please fill all fields!"
        )

        return

    # Check if age is numeric
    if not student_age.isdigit():

        # Show warning
        messagebox.showwarning(
            "Invalid Age",
            "Age must contain numbers only!"
        )

        return

    # Hide login frame
    login_frame.pack_forget()

    # Display exam frame
    exam_frame.pack(fill="both", expand=True)

    # Load first question
    load_question()

    # Start timer
    update_timer()


# Function for restarting exam

def restart_exam():

    # Restart application completely
    root.destroy()


# =========================
# LOGIN PAGE
# =========================

# Create login frame
login_frame = tk.Frame(root, bg="#0f172a")

# Display login frame
login_frame.pack(fill="both", expand=True)

# Create title label
login_title = tk.Label(
    login_frame,
    text="CHEMISTRY EXAM SYSTEM",
    font=("Helvetica", 28, "bold"),
    fg="#38bdf8",
    bg="#0f172a"
)

# Display title
login_title.pack(pady=30)

# Create subtitle
login_subtitle = tk.Label(
    login_frame,
    text="Student Information",
    font=("Verdana", 18),
    fg="white",
    bg="#0f172a"
)

# Display subtitle
login_subtitle.pack(pady=10)

# Create name label
name_label = tk.Label(
    login_frame,
    text="Full Name",
    font=("Verdana", 14, "bold"),
    fg="white",
    bg="#0f172a"
)

# Display name label
name_label.pack(pady=5)

# Create name entry
name_entry = tk.Entry(
    login_frame,
    font=("Verdana", 14),
    width=30,
    justify="center"
)

# Display name entry
name_entry.pack(pady=10)

# Create age label
age_label = tk.Label(
    login_frame,
    text="Age",
    font=("Verdana", 14, "bold"),
    fg="white",
    bg="#0f172a"
)

# Display age label
age_label.pack(pady=5)

# Create age entry
age_entry = tk.Entry(
    login_frame,
    font=("Verdana", 14),
    width=30,
    justify="center"
)

# Display age entry
age_entry.pack(pady=10)

# Create ID label
id_label = tk.Label(
    login_frame,
    text="Student ID",
    font=("Verdana", 14, "bold"),
    fg="white",
    bg="#0f172a"
)

# Display ID label
id_label.pack(pady=5)

# Create ID entry
id_entry = tk.Entry(
    login_frame,
    font=("Verdana", 14),
    width=30,
    justify="center"
)

# Display ID entry
id_entry.pack(pady=10)

# Create start button
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

# Display start button
start_button.pack(pady=30)


# =========================
# EXAM PAGE
# =========================

# Create exam frame
exam_frame = tk.Frame(root, bg="#111827")

# Create timer label
timer_label = tk.Label(
    exam_frame,
    text="Time Left: 05:00",
    font=("Helvetica", 16, "bold"),
    fg="#f87171",
    bg="#111827"
)

# Display timer label
timer_label.pack(pady=15)

# Create progress label
progress_label = tk.Label(
    exam_frame,
    text="",
    font=("Verdana", 14, "bold"),
    fg="#38bdf8",
    bg="#111827"
)

# Display progress label
progress_label.pack(pady=10)

# Create question label
question_label = tk.Label(
    exam_frame,
    text="",
    font=("Helvetica", 20, "bold"),
    fg="white",
    bg="#111827",
    wraplength=700,
    justify="center"
)

# Display question label
question_label.pack(pady=30)

# Store option buttons
option_buttons = []

# Create answer buttons
for i in range(4):

    # Create answer button
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

    # Display answer button
    btn.pack(pady=10)

    # Store button
    option_buttons.append(btn)

# Create navigation frame
nav_frame = tk.Frame(exam_frame, bg="#111827")

# Display navigation frame
nav_frame.pack(pady=30)

# Create previous button
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

# Display previous button
prev_button.pack(side="left", padx=20)

# Create next button
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

# Display next button
next_button.pack(side="right", padx=20)


# =========================
# RESULT PAGE
# =========================

# Create result frame
result_frame = tk.Frame(root, bg="#020617")

# Create result title
result_title = tk.Label(
    result_frame,
    text="",
    font=("Helvetica", 28, "bold"),
    fg="#22c55e",
    bg="#020617"
)

# Display result title
result_title.pack(pady=30)

# Create result information label
result_info = tk.Label(
    result_frame,
    text="",
    font=("Verdana", 16),
    fg="white",
    bg="#020617",
    justify="left"
)

# Display result information
result_info.pack(pady=20)

# Create exit button
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

# Display exit button
exit_button.pack(pady=20)

# Create restart button
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

# Display restart button
restart_button.pack(pady=10)


# =========================
# RUN PROGRAM
# =========================

# Start main application loop
root.mainloop()
