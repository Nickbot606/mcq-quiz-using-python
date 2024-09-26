import tkinter as tk
from tkinter import messagebox as mb
import json

class Quiz:
    def __init__(self):
        self.q_no = 0
        self.display_title()
        self.datasize = len(question)
        self.correct = 0
        
        # Initialize the list of BooleanVar once
        self.opt_selected = [tk.BooleanVar() for _ in range(5)]
        self.opts = self.check_boxes()
        
        self.display_question()
        self.display_options()
        self.buttons()

        # Keyboard bindings
        root.bind('<Return>', lambda event: self.next_btn())  # Enter key
        root.bind('<a>', lambda event: self.select_option(0))
        root.bind('<b>', lambda event: self.select_option(1))
        root.bind('<c>', lambda event: self.select_option(2))
        root.bind('<d>', lambda event: self.select_option(3))
        root.bind('<e>', lambda event: self.select_option(4))

    def clear_previous_question(self):
        for i in range(5):
            self.opt_selected[i].set(False)

    def display_result(self):
        wrong_count = self.datasize - self.correct
        score = int(self.correct / self.datasize * 100)
        result = f"Score {score}%\nCorrect: {self.correct}\nWrong: {wrong_count}"
        mb.showinfo("Result", result)

    def check_ans(self, q_no):
        selected_answers = [var.get() for var in self.opt_selected]
        correct_answers = answer[q_no]

        selected_indices = [i + 1 for i, selected in enumerate(selected_answers) if selected]

        if isinstance(correct_answers, list):
            if sorted(selected_indices) == sorted(correct_answers):
                print("RIGHT!")
                return True
        else:
            if selected_indices == [correct_answers]:
                print("RIGHT!")
                return True
        
        print("WRONG!\n")
        print("You answered: " + str(selected_indices))
        print(question[q_no])

        if isinstance(correct_answers, list):
            for x in correct_answers:
                print(options[q_no][x-1])
        else:
            print(options[q_no][correct_answers-1])
        return False

    def next_btn(self):
        if self.check_ans(self.q_no):
            self.correct += 1
        self.q_no += 1
        if self.q_no == self.datasize:
            self.display_result()
            root.destroy()
        else:
            self.display_question()
            self.clear_previous_question()
            self.display_options()

    def buttons(self):
        next_buttons = tk.Button(root, text="Next", command=self.next_btn, width=10, bg="black", fg="white", font=("arial", 16, "bold"))
        next_buttons.place(x=350, y=380)
        quit_buttons = tk.Button(root, text="Quit", command=root.destroy, width=5, bg="black", fg="white", font=("arial", 16, "bold"))
        quit_buttons.place(x=700, y=50)

    def display_question(self):
        for widget in root.winfo_children():
            if isinstance(widget, tk.Label) and widget.winfo_y() >= 100:
                widget.destroy()
        
        q_no = tk.Label(root, text=question[self.q_no], width=300, wraplength=600, font=("arial", 10, "bold"), anchor="w")
        q_no.place(x=70, y=100)

    def display_title(self):
        title = tk.Label(text="MCQ Quiz", width=50, bg="green", fg="red", font=("arial", 20, "bold"))
        title.place(x=0, y=2)

    def display_options(self):
        # Get the height of the question label
        question_label = root.winfo_children()[-1]  # The last child should be the question label
        question_height = question_label.winfo_height()
        
        base_y = 100 + question_height + 80  # Start below the question, with a bit of padding
        for i in range(5):
            if i < len(options[self.q_no]):
                self.opts[i]["text"] = options[self.q_no][i]
                self.opts[i].place(x=180, y=base_y + (i * 40))
                self.opts[i].select() if self.opt_selected[i].get() else self.opts[i].deselect()
                self.opts[i].config(state=tk.NORMAL)
            else:
                self.opts[i].place_forget()  # Hide option if not present

    def check_boxes(self):
        q_list = []
        for i in range(5):
            radio_btn = tk.Checkbutton(root, text="", variable=self.opt_selected[i], font=("arial", 10))
            q_list.append(radio_btn)
        return q_list

    def select_option(self, index):
        if index < len(self.opts) and self.opts[index].cget("state") != "disabled":
            self.opt_selected[index].set(not self.opt_selected[index].get())
            self.opts[index].select() if self.opt_selected[index].get() else self.opts[index].deselect()

# Load data from JSON
with open("practice-exam-15.json", "r") as f:
    data = json.load(f)

question = data["question"]
answer = data["answer"]
options = data["options"]

# Start quiz
root = tk.Tk()
root.title("MCQ QUIZ")
root.geometry("800x450")
root.resizable(True, True)

quiz = Quiz()
root.mainloop()
