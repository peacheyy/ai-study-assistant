import json
import os
from openai import OpenAI
from tkinter import Tk, filedialog, simpledialog, messagebox
from tkinter.ttk import Style, Button
from convert_to_json import extract_json_objects
from flashcard_gui import FlashcardApp

# Directory to store flashcard sets
FLASHCARDS_DIR = "flashcards"

def configure_button_style(root):
    # Configure the style for buttons in the application
    style = Style(root)
    style.theme_use('default')  # Ensure we're using a consistent theme
    style.configure('RoundedButton.TButton', padding=10, relief="solid", 
                    background="white", foreground="black", 
                    borderwidth=1, bordercolor="gray",
                    font=('Helvetica', 14))
    style.map('RoundedButton.TButton',
              background=[('active', '#f0f0f0')])

def create_styled_root():
    # Create a new Tkinter root with the configured style
    root = Tk()
    configure_button_style(root)
    return root

def ensure_flashcards_dir():
    # Ensure that the flashcards directory exists
    os.makedirs(FLASHCARDS_DIR, exist_ok=True)

def open_file(title="Select a File"):
    # Open a file dialog and return the selected file path
    root = create_styled_root()
    root.withdraw()
    file_path = filedialog.askopenfilename(initialdir="./", title=title)
    root.destroy()
    return file_path

def get_output_file_name():
    # Prompt the user for a filename and return the full path for the new flashcard set
    root = create_styled_root()
    root.withdraw()
    while True:
        file_name = simpledialog.askstring("Input", "Enter a name for your flashcard set (without .json):", parent=root)
        if file_name and file_name.strip():
            root.destroy()
            return os.path.join(FLASHCARDS_DIR, f"{file_name.strip()}.json")
        print("Please enter a valid name.")

def generate_flashcards(file_path):
    # Generate flashcards using OpenAI's API based on the content of the given file
    client = OpenAI()

    # Create an AI assistant for generating flashcards
    assistant = client.beta.assistants.create(
        name="Study Assistant",
        instructions="""You are an intelligent study assistant designed to help students with their studies.
        Your primary role is to provide information from the study materials provided.""",
        model="gpt-4-1106-preview",
        tools=[{"type": "file_search"}],
    )

    # Upload the study material file
    with open(file_path, "rb") as file_stream:
        message_file = client.files.create(
            file=file_stream, purpose="assistants"
        )

    # Create a thread with instructions for generating flashcards
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": """You are a study assistant designed to help students learn by generating flashcards from the provided study materials. 
                When generating flashcards, always use the following JSON format without any code block markers or additional formatting:

                {"id": "", "front": "<The question, prompt, or term to be placed on the front of the flashcard>", "back": "<The answer, explanation, or definition to be placed on the back of the flashcard>"}

                Please ensure that:
                1. The "id" field is left empty (as an empty string).
                2. The content for "front" and "back" fields is filled in appropriately.
                3. Each flashcard is on a single line, with no line breaks within the JSON object.
                4. There are no additional spaces or formatting characters outside of the JSON object.""",
                "attachments": [{"file_id": message_file.id, "tools": [{"type": "file_search"}]}]
            }
        ]
    )

    # Run the assistant to generate flashcards
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id, assistant_id=assistant.id
    )

    # Extract the generated flashcards from the assistant's response
    messages = client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id)
    message_content = messages.data[0].content[0].text.value

    return extract_json_objects(message_content)

def update_flashcards_json(new_flashcards, output_file):
    # Update the flashcards JSON file with new flashcards
    try:
        existing_flashcards = []
        if os.path.exists(output_file):
            with open(output_file, 'r') as json_file:
                existing_flashcards = json.load(json_file)
        
        existing_flashcards.extend(new_flashcards)

        with open(output_file, 'w') as json_file:
            json.dump(existing_flashcards, json_file, indent=4)

        print(f"Total flashcards in {output_file}: {len(existing_flashcards)}")
    except Exception as e:
        print(f"An error occurred while updating the flashcards: {e}")

def get_user_choice():
    # Display a GUI to let the user choose between generating new flashcards or using existing ones
    root = create_styled_root()
    root.title("Flashcard App")

    choice = [None]

    def make_choice(value):
        choice[0] = value
        root.quit()

    Button(root, text="Generate New Flashcards", command=lambda: make_choice(True), style='RoundedButton.TButton').pack(side="left", padx=20, pady=20)
    Button(root, text="Use Existing Flashcards", command=lambda: make_choice(False), style='RoundedButton.TButton').pack(side="right", padx=20, pady=20)

    root.protocol("WM_DELETE_WINDOW", lambda: make_choice(None))
    root.mainloop()
    root.destroy()

    return choice[0]

def main():
    # Main function to run the flashcard application
    ensure_flashcards_dir()
    generate_new = get_user_choice()

    if generate_new:
        # Generate new flashcards
        file_path = open_file("Select study material")
        if not file_path:
            print("No file selected. Exiting.")
            return

        print("Generating flashcards...")
        new_flashcards = generate_flashcards(file_path)

        output_file = get_output_file_name()
        print(f"Updating {output_file}...")
        update_flashcards_json(new_flashcards, output_file)

    # Run the flashcard GUI application
    print("Starting flashcard app...")
    root = create_styled_root()
    app = FlashcardApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()