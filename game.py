import tkinter as tk
import random
import csv
import time

# List of possible words
words = open("words.csv")
word_raw = csv.reader(words)
word_list = [word[0] for word in word_raw]

class WordleGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wordle")
        self.geometry("800x700")
        self.attempts = 6
        self.points = 0
        self.current_word = random.choice(word_list)
        self.word_guess = tk.StringVar()

        self.create_widgets()
        self.restart_game()

    def create_widgets(self):
        self.word_rows = []
        for row in range(6):
            row_frame = tk.Frame(self)
            row_frame.pack(pady=5)

            word_labels = []
            for i in range(5):
                letter_label = tk.Label(row_frame, text="", font=("Arial", 18), width=2, height=1, relief=tk.RAISED, bg="white")
                letter_label.pack(side=tk.LEFT, padx=3)
                word_labels.append(letter_label)

            self.word_rows.append(word_labels)

        self.entry = tk.Entry(self, textvariable=self.word_guess, font=("Arial", 16))
        self.entry.pack(pady=10)

        self.check_button = tk.Button(self, text="Check", command=self.check_word, font=("Arial", 14), bg="#00C853", fg="black", activebackground="#00B049")
        self.check_button.pack(pady=10)

        # Limit entry to 5 alphabetical characters only
        self.entry.config(validate="key", validatecommand=(self.register(self.on_validate), "%P"))

        # Remaining attempts label
        self.remaining_attempts_label = tk.Label(self, text=f"Remaining Attempts: {self.attempts}", font=("Arial", 14))
        self.remaining_attempts_label.pack(pady=5)

        # Congrats label
        self.congrats_label = tk.Label(self, text="", font=("Arial", 16))
        self.congrats_label.pack(pady=10)

        # Invalid word label
        self.invalid_word_label = tk.Label(self, text="", font=("Arial", 16), fg="red")
        self.invalid_word_label.pack(pady=10)

        # Points label
        self.points_label = tk.Label(self, text="Points: 0", font=("Arial", 14))
        self.points_label.pack(pady=5)

        # On-screen keyboard
        self.keyboard_frame = tk.Frame(self, bg="lightgray")
        self.keyboard_frame.pack(pady=10)

        keyboard_rows = [
            "qwertyuiop",
            "asdfghjkl",
            "zxcvbnm"
        ]

        self.letter_buttons = {}
        for i, row in enumerate(keyboard_rows):
            row_frame = tk.Frame(self.keyboard_frame)
            row_frame.pack()
            for letter in row:
                btn = tk.Button(row_frame, text=letter.upper(), font=("Arial", 14), width=2, height=1, bg="lightblue", command=lambda l=letter: self.add_letter(l))
                btn.pack(side=tk.LEFT, padx=3, pady=3)
                self.letter_buttons[letter] = btn

    def add_letter(self, letter):
        current_guess = self.word_guess.get()
        if len(current_guess) < 5:
            self.word_guess.set(current_guess + letter)
            self.letter_buttons[letter].config(bg="gray", state=tk.DISABLED)

    def on_validate(self, new_text):
        if len(new_text) > 5:
            return False
        if new_text and not new_text.isalpha():
            return False
        return True

    def check_word(self):
        guess = self.word_guess.get().lower()

        if len(guess) != 5:
            self.invalid_word_label.config(text="Please enter a five-letter word.")
            return

        if guess not in word_list:
            self.invalid_word_label.config(text="Please enter a valid word from the list.")
            return

        if guess == self.current_word:
            self.congrats_label.config(text="Congratulations! You guessed the word!", fg="green")
            self.points += 10  # Add 10 points for correct guess
            self.points_label.config(text=f"Points: {self.points}")
            self.after(3000, self.restart_game)  # Display congratulatory message for 3 seconds
        else:
            self.attempts -= 1
            self.remaining_attempts_label.config(text=f"Remaining Attempts: {self.attempts}")
            if self.attempts == 0:
                self.congrats_label.config(text=f"Game Over! The word was '{self.current_word}'.", fg="red")
                self.restart_game()
            else:
                self.update_word_display(guess)

    def update_word_display(self, guess):
        row_index = 5 - self.attempts
        for i, letter_label in enumerate(self.word_rows[row_index]):
            letter = self.current_word[i]
            if guess[i] == letter:
                letter_label.config(text=guess[i], bg="#00C853", fg="white")
            elif guess[i] in self.current_word:
                letter_label.config(text=guess[i], bg="#FFD600", fg="black")
            else:
                letter_label.config(text=guess[i], bg="#333333", fg="white")
            self.update()
            self.after(500)  # Add a delay of 0.5 seconds for each letter update

        self.restart_guess()

    def restart_guess(self):
        self.word_guess.set("")
        self.invalid_word_label.config(text="")
        for letter in "abcdefghijklmnopqrstuvwxyz":
            self.letter_buttons[letter].config(bg="lightblue", state=tk.NORMAL)

    def restart_game(self):
        self.attempts = 6
        self.current_word = random.choice(word_list)
        self.congrats_label.config(text="")
        self.remaining_attempts_label.config(text=f"Remaining Attempts: {self.attempts}")
        self.points_label.config(text="Points: 0")
        for row in self.word_rows:
            for letter_label in row:
                letter_label.config(text="", bg="white")

if __name__ == "__main__":
    app = WordleGame()
    app.mainloop()
