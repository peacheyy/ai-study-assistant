import json
import random
import os
from tkinter import Tk, Label, Frame, filedialog
from tkinter.ttk import Style, Button as TButton

FLASHCARDS_DIR = "flashcards"

class FlashcardApp:
    def __init__(self, master):
        self.master = master
        master.title("Flashcard App")

        self.configure_styles()

        self.flashcards = self.load_flashcards()
        if not self.flashcards:
            self.master.quit()
            return

        self.current_card = None

        self.frame = Frame(master)
        self.frame.pack(pady=20)

        self.card_frame = Frame(self.frame, width=400, height=200, bg="white", relief="raised", borderwidth=2)
        self.card_frame.pack(pady=20)
        self.card_frame.pack_propagate(False)  # This ensures the frame stays at the size we set

        self.card_text = Label(self.card_frame, text="", wraplength=380, font=("Arial", 14), bg="white")
        self.card_text.pack(expand=True, fill="both")
        self.card_text.bind("<Button-1>", self.flip_card)  # Bind click event to flip_card

        self.next_button = TButton(self.frame, text="Next", command=self.next_card, style='RoundedButton.TButton')
        self.next_button.pack(side="bottom", pady=10)

        self.is_front = True
        self.next_card()

    def configure_styles(self):
        style = Style()
        style.configure('RoundedButton.TButton', padding=10, relief="solid", 
                        background="white", foreground="black", 
                        borderwidth=1, bordercolor="gray",
                        font=('Helvetica', 12))
        style.map('RoundedButton.TButton',
                  background=[('active', '#f0f0f0')])

    def load_flashcards(self):
        file_path = filedialog.askopenfilename(
            initialdir=FLASHCARDS_DIR,
            title="Select flashcard set",
            filetypes=(("JSON files", "*.json"), ("all files", "*.*"))
        )
        if not file_path:
            print("No file selected. Exiting.")
            return []

        with open(file_path, 'r') as file:
            return json.load(file)

    def next_card(self):
        if not self.flashcards:
            self.card_text.config(text="No flashcards available")
            return

        self.current_card = random.choice(self.flashcards)
        self.is_front = True
        self.update_display()

    def flip_card(self, event=None):  # Added event parameter for click binding
        self.is_front = not self.is_front
        self.update_display()

    def update_display(self):
        if not self.current_card:
            return

        if self.is_front:
            self.card_text.config(text=self.current_card['front'])
            self.card_frame.config(bg="white")
            self.card_text.config(bg="white")
        else:
            self.card_text.config(text=self.current_card['back'])
            self.card_frame.config(bg="light yellow")
            self.card_text.config(bg="light yellow")

def run_flashcard_app():
    root = Tk()
    app = FlashcardApp(root)
    root.mainloop()

if __name__ == "__main__":
    run_flashcard_app()