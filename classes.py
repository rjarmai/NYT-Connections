import collections
import random
from tkinter import *

BACKGROUND = '#EFEFE6'
CLICKED_ON_BACKGROUND = '#5A594E'
FONT = 'Franklin Gothic'

class Category:

    def __init__(self, words, color, explanation):
        self.words = words
        self.color = color
        self.explanation = explanation


class ConnectionsGame:

    def __init__(self, categories):
        self.categories = categories
        self.words_remaining = [word for category in self.categories for word in category.words]
        self.mistakes_remaining = 4
        self.texts_chosen = []
        self.boxes_chosen = []
        self.guessed_categories = []
        self.categories_guessed_num = 0
        self.background = BACKGROUND
        self.clicked_on_background = CLICKED_ON_BACKGROUND

        random.shuffle(self.words_remaining)

        self.root = Tk()
        self.root.configure(bg='white')

        self.boxes = []
        for row in range(4):
            for col in range(4):
                word_index = row * 4 + col
                word = self.words_remaining[word_index]

                btn = Button(self.root, text=word, width=20, height=5, bg=self.background, font=(FONT, 12, "bold"))
                btn.config(command=lambda b=btn, w=word: self.select_box(b, w))
                btn.grid(row=row, column=col, padx=5, pady=5)

                self.boxes.append(btn)

        self.submit_button = Button(text="Submit",
                                    width=10,
                                    pady=5,
                                    command=self.submit_guess,
                                    font=(FONT, 8, "bold"))

        self.submit_button.grid(row=4, column=1, columnspan=2)

        self.mistakes_display = Canvas(width=200, height=20, bg='white', highlightthickness=0)
        self.mistakes_display.create_text(45, 10, text='Mistakes', font=(FONT, 12, "bold"))
        self.mistake_circles = []
        for i in range(4):
            circle = self.mistakes_display.create_oval(20*i+90, 5 , 20*i+100, 15, fill=CLICKED_ON_BACKGROUND, outline=CLICKED_ON_BACKGROUND)
            self.mistake_circles.append(circle)
        self.mistakes_display.grid(row=5, column=1, columnspan=2)
        self.root.mainloop()


    def select_box(self, button, word):
        if button['bg'] == self.background and len(self.boxes_chosen) < 4:
            button.config(bg=self.clicked_on_background, fg='white')
            self.boxes_chosen.append(button)
            self.texts_chosen.append(word)

        elif button['bg'] == self.clicked_on_background:
            button.config(bg=self.background, fg='black')
            self.boxes_chosen.remove(button)
            self.texts_chosen.remove(word)

    def submit_guess(self):
        if len(self.boxes_chosen) == 4:
            is_correct = False
            for category in self.categories:
                if collections.Counter(self.texts_chosen) == collections.Counter(category.words):
                    is_correct = True
                    self.guessed_categories.append(category)
                    self.categories_guessed_num += 1
                    self.reveal(category)
                    break
            if not is_correct:
                self.mistakes_remaining -= 1
                self.mistakes_display.delete(self.mistake_circles[-1])
                self.mistake_circles.pop(-1)
            if self.mistakes_remaining == 0:
                self.end_game()

    def reveal(self, category):
        for text in self.texts_chosen:
            self.words_remaining.remove(text)

        for box in self.boxes_chosen:
            box.destroy()
            self.boxes.remove(box)

        self.boxes_chosen.clear()
        self.texts_chosen.clear()

        solution = Canvas(self.root, width=800, height=100, bg=category.color)
        solution.create_text(400, 75, text=(', '.join(category.words)), font=(FONT, 16, "italic"))
        solution.create_text(400, 35, text=category.explanation, font=(FONT, 20, "bold"))
        solution.grid(row=self.categories_guessed_num - 1, column=0, columnspan=4)


        self.boxes.reverse()

        current_row = self.categories_guessed_num
        current_col = 0

        for box in self.boxes:
            box.grid(row=current_row, column=current_col)
            current_col += 1
            if current_col > 3:
                current_col = 0
                current_row += 1

    def end_game(self):
        self.root.update()
        self.root.minsize(self.root.winfo_width(), self.root.winfo_height())


        for box in self.boxes_chosen:
            box.config(bg=self.background, fg='black')

        for box in self.boxes:
            box.config(state="disabled")
        self.submit_button.config(state="disabled")
        self.mistakes_display.destroy()

        missed_categories = [cat for cat in self.categories if cat not in self.guessed_categories]

        delay = 500
        for category in missed_categories:
            self.root.after(delay, lambda cat=category: self._draw_solution_banner(cat))
            delay += 1000

    def _draw_solution_banner(self, category):
        buttons_to_remove = []
        for box in self.boxes:
            if box.cget("text") in category.words:
                buttons_to_remove.append(box)

        for box in buttons_to_remove:
            box.destroy()
            self.boxes.remove(box)

        solution = Canvas(self.root, width=800, height=100, bg=category.color)
        solution.create_text(400, 35, text=category.explanation, font=(FONT, 20, "bold"))
        solution.create_text(400, 75, text=(', '.join(category.words)), font=(FONT, 16, "italic"))

        solution.grid(row=self.categories_guessed_num, column=0, columnspan=4)
        self.categories_guessed_num += 1

        current_row = self.categories_guessed_num
        current_col = 0
        for box in self.boxes:
            box.grid(row=current_row, column=current_col, padx=5, pady=5)
            current_col += 1
            if current_col > 3:
                current_col = 0
                current_row += 1
