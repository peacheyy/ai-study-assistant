import json
import random
from tkinter import Tk, Label, Frame, filedialog, messagebox
from tkinter.ttk import Style, Button as TButton

FLASHCARDS_DIR = "flashcards"

def configure_button_style(root):
    # Configure the style for buttons in the application
    style = Style(root)
    style.theme_use('default')  # Ensure we're using a consistent theme
    style.configure('RoundedButton.TButton', padding=10, relief="solid", 
                    background="white", foreground="black", 
                    borderwidth=1, bordercolor="gray",
                    font=('Helvetica', 12))
    style.map('RoundedButton.TButton', background=[('active', '#f0f0f0')])

class FlashcardApp:
    def __init__(self, master):
        # Initialize the Flashcard application
        self.master = master
        master.title("Flashcard App")

        configure_button_style(self.master)

        self.flashcards = self.load_flashcards()
        if not self.flashcards:
            self.master.quit()
            return

        self.current_index = -1
        self.unknown_cards = set()
        self.review_mode = False
        self.is_front = True

        self.setup_ui()

    def setup_ui(self):
        # Set up the user interface for the flashcard app
        self.frame = Frame(self.master)
        self.frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Top frame with Change Set and Review Unknown buttons
        top_frame = Frame(self.frame)
        top_frame.pack(fill="x", pady=(0, 10))

        self.change_set_button = TButton(top_frame, text="Change Set", command=self.change_set, style='RoundedButton.TButton')
        self.change_set_button.pack(side="left")

        self.review_button = TButton(top_frame, text="Review Unknown", command=self.start_review, style='RoundedButton.TButton')
        self.review_button.pack(side="right")

        # Flashcard display area
        self.card_frame = Frame(self.frame, width=400, height=200, bg="white", relief="raised", borderwidth=2)
        self.card_frame.pack(expand=True, fill="both", pady=10)
        self.card_frame.pack_propagate(False)

        self.card_text = Label(self.card_frame, text="", wraplength=380, font=("Arial", 14), bg="white")
        self.card_text.pack(expand=True, fill="both")
        self.card_text.bind("<Button-1>", self.flip_card)

        # Bottom frame with Know and Don't Know buttons
        button_frame = Frame(self.frame)
        button_frame.pack(side="bottom", pady=(10, 0))

        self.unknown_button = TButton(button_frame, text="Don't Know", command=lambda: self.mark_card(False), style='RoundedButton.TButton')
        self.unknown_button.pack(side="left", padx=5)

        self.known_button = TButton(button_frame, text="Know", command=lambda: self.mark_card(True), style='RoundedButton.TButton')
        self.known_button.pack(side="right", padx=5)

        self.next_card()

    def load_flashcards(self):
        # Load flashcards from a JSON file selected by the user
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
        # Move to the next flashcard, handling review mode and set completion
        if not self.flashcards:
            self.card_text.config(text="No flashcards available")
            return

        if self.review_mode and not self.unknown_cards:
            self.end_review()
            return

        if not self.review_mode and self.current_index == len(self.flashcards) - 1:
            self.end_set()
            return

        self.current_index = self.unknown_cards.pop() if self.review_mode else self.current_index + 1
        self.is_front = True
        self.update_display()

    def end_review(self):
        # Handle the end of the review mode
        messagebox.showinfo("Review Complete", "You've reviewed all unknown cards!")
        self.review_mode = False
        self.unknown_cards = set()
        self.restart_set()

    def end_set(self):
        # Handle reaching the end of the flashcard set
        if self.unknown_cards and messagebox.askyesno("Review", "You've finished the set. Do you want to review unknown cards?"):
            self.start_review()
        else:
            self.restart_set()

    def restart_set(self):
        # Offer to restart the flashcard set or end the session
        if messagebox.askyesno("Restart", "Do you want to start over with the full set?"):
            self.current_index = -1
            self.unknown_cards = set()
            self.next_card()
        else:
            messagebox.showinfo("Completed", "Congratulations! You've completed the set.")
            self.card_text.config(text="Set completed. Choose 'Change Set' to load a new set.")

    def flip_card(self, event=None):
        # Flip the current flashcard to show the other side
        self.is_front = not self.is_front
        self.update_display()

    def update_display(self):
        # Update the display with the current flashcard's content
        if not self.flashcards:
            return

        current_card = self.flashcards[self.current_index]
        text = current_card['front'] if self.is_front else current_card['back']
        bg_color = "white" if self.is_front else "light yellow"

        self.card_text.config(text=text)
        self.card_frame.config(bg=bg_color)
        self.card_text.config(bg=bg_color)

    def change_set(self):
        # Change the current flashcard set
        new_flashcards = self.load_flashcards()
        if new_flashcards:
            self.flashcards = new_flashcards
            self.current_index = -1
            self.unknown_cards = set()
            self.review_mode = False
            self.next_card()
        else:
            self.card_text.config(text="No flashcards available")

    def mark_card(self, known):
        # Mark the current card as known or unknown and move to the next card
        if not known:
            self.unknown_cards.add(self.current_index)
        self.next_card()

    def start_review(self):
        # Start the review mode for unknown cards
        if self.unknown_cards:
            self.review_mode = True
            self.unknown_cards = set(self.unknown_cards)  # Create a copy to modify during review
            self.next_card()
        else:
            messagebox.showinfo("Review", "No cards marked for review!")

def run_flashcard_app():
    # Initialize and run the Flashcard application
    root = Tk()
    app = FlashcardApp(root)
    root.mainloop()

if __name__ == "__main__":
    run_flashcard_app()