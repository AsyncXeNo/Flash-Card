import tkinter as tk
from data import WordsData


class Application(object):
    def __init__(self):
        self.data = WordsData("data/french_words.csv")
        self.current_entry = None
        self.can_mark = False
        self.score = 0
        self.count = 0
        self.end = False

        headers = self.data.get_headers()
        self.front_lang = headers[0]
        self.back_lang = headers[1]

        self.window = tk.Tk()
        self.window.title("Flash Card!")
        self.window.config(padx=50, pady=50, bg="#B1DDC6")

        self.front = tk.PhotoImage(file="images/card_front.png")
        self.back = tk.PhotoImage(file="images/card_back.png")
        self.right = tk.PhotoImage(file="images/right.png")
        self.wrong = tk.PhotoImage(file="images/wrong.png")

        self.canvas = tk.Canvas(width=800, height=526, highlightthickness=0, bg="#B1DDC6")
        self.card = self.canvas.create_image(400, 263, image=self.front)
        self.language = self.canvas.create_text(400, 150, text="Language", fill="black", font=("Arial", 40, "italic"))
        self.word = self.canvas.create_text(400, 263, text="word", fill="black", font=("Arial", 60, "bold"))
        self.info = self.canvas.create_text(400, 400, fill="red", text="Be honest! Tick if you're right and cross if you're wrong.", font=("Arial", 20))
        self.countdown = self.canvas.create_text(400, 460, text="5", fill="black", font=("Arial", 30))
        self.canvas.grid(column=0, row=0, columnspan=2)

        self.right_button = tk.Button(image=self.right, highlightthickness=0, borderwidth=0, bg="#B1DDC6", activebackground="#B1DDC6", command=self.mark_right)
        self.right_button.grid(column=0, row=1)

        self.wrong_button = tk.Button(image=self.wrong, highlightthickness=0, borderwidth=0, bg="#B1DDC6", activebackground="#B1DDC6", command=self.mark_wrong)
        self.wrong_button.grid(column=1, row=1)

        self.window.after(1000, self.start, 4)
        self.window.mainloop()

    def start(self, count):
        self.canvas.itemconfig(self.countdown, text=count)
        if count == 0:
            self.create_new_card()
            self.window.after(100, self.remove_countdown)
        else:
            self.window.after(1000, self.start, count-1)

    def remove_countdown(self):
        self.canvas.itemconfig(self.countdown, text="")
        self.canvas.itemconfig(self.info, text="")

    def mark_right(self):
        if self.end:
            self.window.destroy()
        if self.can_mark:
            self.score += 1
            self.count += 1
            self.create_new_card()

    def mark_wrong(self):
        if self.end:
            self.window.destroy()
        if self.can_mark:
            self.count += 1
            self.create_new_card()

    def create_new_card(self):
        self.can_mark = False
        self.current_entry = self.data.get_entry()
        if self.current_entry:
            self.canvas.itemconfig(self.card, image=self.front)
            self.canvas.itemconfig(self.language, text=self.front_lang)
            self.canvas.itemconfig(self.word, text=self.current_entry["front"])
            self.window.after(2000, self.turn_card)
        else:
            self.canvas.itemconfig(self.language, text="Your Score")
            self.canvas.itemconfig(self.word, text=f"{self.score}/{self.count}")
            self.end = True

    def turn_card(self):
        self.can_mark = True
        self.canvas.itemconfig(self.card, image=self.back)
        self.canvas.itemconfig(self.language, text=self.back_lang)
        self.canvas.itemconfig(self.word, text=self.current_entry["back"])
