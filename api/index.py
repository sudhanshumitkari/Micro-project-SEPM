from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Load quiz data
try:
    with open("GUI_Quiz.json") as f:
        obj = json.load(f)
    q = obj['questions']
    options = obj['options']
    a = obj['ans']
    assert len(q) == len(options) == len(a)
except Exception as e:
    root = Tk()
    root.withdraw()
    mb.showerror("Error", f"Could not load quiz data:\n{e}")
    exit()

# Root window setup
root = Tk()
root.geometry("900x700")
root.title("Python Quiz")
root.configure(bg="#2E2E2E")

# Style setup
style = ttk.Style()
style.theme_use("clam")

style.configure("TButton",
                font=("Segoe UI", 12, "bold"),
                foreground="white",
                background="#3F51B5",
                padding=10)
style.map("TButton",
          background=[("active", "#303F9F")])

style.configure("TLabel", font=("Segoe UI", 14), background="#2E2E2E", foreground="white")
style.configure("Title.TLabel", font=("Segoe UI", 24, "bold"), foreground="white", background="#2E2E2E")

# Login Page Class
class LoginPage:
    def __init__(self):
        self.login_frame = Frame(root, bg="#393E46", bd=2, relief=RIDGE)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=350)

        ttk.Label(self.login_frame, text="🔐 Login to Start Quiz", style="Title.TLabel").pack(pady=(20, 10))

        ttk.Label(self.login_frame, text="Username", background="#393E46", foreground="white",
                  font=("Segoe UI", 12)).pack(pady=(10, 5))
        self.username_entry = Entry(self.login_frame, font=("Segoe UI", 13), width=30)
        self.username_entry.pack(pady=5)

        ttk.Label(self.login_frame, text="Password", background="#393E46", foreground="white",
                  font=("Segoe UI", 12)).pack(pady=(15, 5))
        self.password_entry = Entry(self.login_frame, show="*", font=("Segoe UI", 13), width=30)
        self.password_entry.pack(pady=5)

        ttk.Button(self.login_frame, text="Login", command=self.login).pack(pady=25)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username and password and username == "dam" and password == "6241":
            self.login_frame.destroy()
            Quiz(username)
        else:
            mb.showerror("Login Failed", "Incorrect username or password.")

# Quiz Class
class Quiz:
    def __init__(self, username):
        self.username = username
        self.qn = 0
        self.correct = 0
        self.time_left = 30
        self.opt_selected = IntVar()
        self.timer_id = None
        self.user_answers = [0] * len(q)
        self.scored = [False] * len(q)

        Label(root, text="🧠 ONLINE PYTHON QUIZ", bg="#2A2A2A", fg="white",
              font=("Helvetica", 20, "bold"), relief=SOLID, bd=2).pack(pady=20)

        self.status_frame = Frame(root, bg="#2E2E2E")
        self.status_frame.pack(pady=10)

        self.timer_label = Label(self.status_frame, text=f"Time left: {self.time_left}s",
                                 fg="gold", font=("Arial", 16, "bold"), bg="#2E2E2E")
        self.timer_label.pack(side=LEFT, padx=10)

        self.progressbar = ttk.Progressbar(self.status_frame, orient="horizontal", length=300, mode="determinate")
        self.progressbar.pack(side=LEFT, padx=20)
        self.progressbar["maximum"] = 30

        self.progress_label = Label(self.status_frame, text="", fg="white", font=("Arial", 16), bg="#2E2E2E")
        self.progress_label.pack(side=RIGHT, padx=10)

        self.ques = Label(root, text=q[self.qn], wraplength=750, justify="left",
                          font=("Segoe UI", 18, "bold"), bg="#2E2E2E", fg="white", anchor="w")
        self.ques.pack(pady=30, padx=20, anchor="w")

        self.opts = self.radiobtns()
        self.display_options(self.qn)
        self.buttons()
        self.countdown()

    def radiobtns(self):
        b = []
        self.radio_frame = Frame(root, bg="#2E2E2E")
        self.radio_frame.pack(pady=20)
        for val in range(4):
            btn = Radiobutton(self.radio_frame, text="", variable=self.opt_selected, value=val + 1,
                              font=("Segoe UI", 14), bg="#2E2E2E", fg="white", anchor="w",
                              selectcolor="#303F9F", activebackground="#2E2E2E",
                              indicatoron=1, padx=10)
            btn.pack(anchor="w", pady=5)
            b.append(btn)
        return b

    def display_options(self, qn):
        self.opt_selected.set(self.user_answers[qn])
        self.ques["text"] = q[qn]
        self.progress_label.config(text=f"Question {qn + 1} of {len(q)}")
        for i in range(4):
            self.opts[i]["text"] = options[qn][i]

    def buttons(self):
        self.btn_frame = Frame(root, bg="#2E2E2E")
        self.btn_frame.pack(pady=30)

        ttk.Button(self.btn_frame, text="Next", command=self.next_btn).grid(row=0, column=0, padx=20)
        ttk.Button(self.btn_frame, text="Back", command=self.back_btn).grid(row=0, column=1, padx=20)
        ttk.Button(self.btn_frame, text="Quit", command=root.destroy).grid(row=0, column=2, padx=20)

    def next_btn(self, auto=False):
        if self.timer_id:
            root.after_cancel(self.timer_id)

        selected = self.opt_selected.get()
        if not auto and selected == 0:
            mb.showwarning("No Selection", "Please select an option before continuing.")
            return

        self.user_answers[self.qn] = selected
        if not self.scored[self.qn] and selected == a[self.qn]:
            self.correct += 1
            self.scored[self.qn] = True

        self.qn += 1
        if self.qn == len(q):
            self.display_result()
        else:
            self.time_left = 30
            self.display_options(self.qn)
            self.countdown()

    def back_btn(self):
        if self.qn > 0:
            self.qn -= 1
            self.time_left = 30
            self.cancel_timer()
            self.display_options(self.qn)
            self.countdown()

    def cancel_timer(self):
        if self.timer_id:
            root.after_cancel(self.timer_id)
            self.timer_id = None

    def countdown(self):
        self.timer_label.config(text=f"Time left: {self.time_left}s")
        self.progressbar["value"] = 30 - self.time_left
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_id = root.after(1000, self.countdown)
        else:
            mb.showinfo("Time's up", "Time for this question is over.")
            self.next_btn(auto=True)

    def display_result(self):
        for widget in root.winfo_children():
            widget.destroy()

        Label(root, text="Quiz Completed ✅", font=("Arial", 24, "bold"),
              bg="#2E2E2E", fg="lightgreen").pack(pady=20)

        Label(root, text=f"User: {self.username}", font=("Segoe UI", 18),
              bg="#2E2E2E", fg="cyan").pack(pady=5)

        score = int(self.correct / len(q) * 100)
        Label(root, text=f"Your Score: {score}%", font=("Segoe UI", 26, "bold"),
              bg="#2E2E2E", fg="#00E676").pack(pady=10)

        Label(root, text=f"Correct Answers: {self.correct}", font=("Segoe UI", 18),
              bg="#2E2E2E", fg="#4FC3F7").pack(pady=5)

        Label(root, text=f"Wrong Answers: {len(q) - self.correct}", font=("Segoe UI", 18),
              bg="#2E2E2E", fg="#FF8A65").pack(pady=5)

        # Display the pie chart
        self.display_pie_chart()

        btn_frame = Frame(root, bg="#2E2E2E")
        btn_frame.pack(pady=40)

        ttk.Button(btn_frame, text="Try Again", command=self.restart_quiz).grid(row=0, column=0, padx=20)
        ttk.Button(btn_frame, text="Exit", command=root.destroy).grid(row=0, column=1, padx=20)

    def display_pie_chart(self):
        labels = ['Correct', 'Incorrect']
        sizes = [self.correct, len(q) - self.correct]
        colors = ['#00E676', '#FF8A65']
        explode = (0.1, 0)  # Explode the first slice (Correct)

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
               shadow=True, startangle=140)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.get_tk_widget().pack(pady=40)
        canvas.draw()

    def restart_quiz(self):
        for widget in root.winfo_children():
            widget.destroy()
        Quiz(self.username)

# Start the app
LoginPage()
root.mainloop()
