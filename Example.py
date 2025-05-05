from tkinter import *
from tkinter import messagebox as mb
import json  

root = Tk()
root.geometry("1000x800")
root.title("Quiz")

with open("GUI_Quiz.json") as f:
   obj = json.load(f)

q = (obj['questions'])
options = (obj['options'])
a = (obj['ans'])
print(q)
print(options)
print(a)
root.configure(bg="purple")

# root.mainloop()

# Now we gonna create labels using class
class Quiz:
   def __init__(self):
      self.qn = 0
      self.ques = self.question(self.qn)



   def question(self,qn):
      self.title = Label(root, text="Let's Check How Much Python You Know", width=90, bg="darkblue", fg="white", font=("times", 22, "bold"))
      self.title.place(x=0, y=4)
      qn = Label(root, text=q[qn], width=97, font=("Arial", 19, "bold"), anchor="w")
      qn.place(x=40, y=130)
      return qn


   def __init__(self):
      self.qn = 0
      self.opt_selected = IntVar()
      self.opts = self.radiobtns()
      self.ques = self.question(self.qn)



   def radiobtns(self):
      val = 0
      b = []
      yp = 200
      while val < 4:
         btn = Radiobutton(root, text="  ", variable=self.opt_selected, value=val + 1, font=("times",17))
         b.append(btn)
         btn.place(x=100, y=yp)
         val +=1
         yp +=60
      return b



   def __init__(self):
      self.qn = 0 
      self.opt_selected=IntVar()
      self.ques = self.question(self.qn)
      self.opts = self.radiobtns()
      self.display_options(self.qn)
      self.buttons()
      self.correct = 0



   def display_options(self, qn):
      val = 0
      self.opt_selected.set(0)
      self.ques["text"] = q[qn]
      for op in options[qn]:
         self.opts[val] ["text"] = op
         val +=1


   
   def buttons(self):
      nbutton = Button(root, text= "Next", command=self.next_btn, width=10, bg="green", fg="white", font=("times", 20, "bold"))
      nbutton.place(x=450, y=500)
      qbutton = Button(root, text= "Quit", command=root.destroy, width=10, bg="red", fg="white", font=("times", 20, "bold"))
      qbutton.place(x=850, y=500)



   def checkans(self, qn):
      if self.opt_selected.get() == a[qn]:
         return True


   def __init__(self):
        self.qn = 0
        self.correct = 0
        self.opt_selected = IntVar()
        self.time_left = 30  # seconds

        self.title = Label(root, text="Quiz in Python Programming", width=90, bg="darkblue", fg="white", font=("times", 20, "bold"))
        self.title.place(x=0, y=4)

        self.timer_label = Label(root, text=f"Time left: {self.time_left}s", width=20, fg="red", font=("Arial", 18, "bold"))
        self.timer_label.place(x=1100, y=510)

        self.ques = Label(root, text=q[self.qn], width=97, font=("Arial", 19, "bold"), anchor="w")
        self.ques.place(x=40, y=130)

        self.opts = self.radiobtns()
        self.display_options(self.qn)
        self.buttons()
        self.countdown()


   def countdown(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time left: {self.time_left}s")
            root.after(1000, self.countdown)
        else:
            self.next_btn(auto=True)



   def next_btn(self, auto=False):
      if not auto and self.checkans(self.qn):
         self.correct += 1
      elif auto and self.opt_selected.get() == a[self.qn]:
         self.correct += 1
      self.qn += 1
      if self.qn == len(q):
         self.display_result()
      else:
         self.time_left = 30  # Reset timer for next question
         self.display_options(self.qn)
         self.countdown()
   

      
   def display_result(self):
      score = int(self.correct / len(q) * 100)
      result = "Score:" + str(score) + "%"
      wc = len(q) - self.correct
      correct = "No. of correct answers:" + str(self.correct)
      wrong = wrong = "No. of wrong answers: " + str(len(q) - self.correct)
      mb.showinfo("Result","\n".join([result, correct, wrong]))
         

quiz = Quiz()
root.mainloop()