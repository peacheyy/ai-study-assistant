import json
import os
from openai import OpenAI
from tkinter import Tk, filedialog, simpledialog, messagebox, Label
from tkinter.ttk import Style, Button
from convert_to_json import extract_json_objects
from flashcard_gui import run_flashcard_app

FLASHCARDS_DIR = "flashcards"

#Function to configure button style
def configure_button_style():
    style = Style()
    style.configure('RoundedButton.TButton', padding=10, relief="solid", 
                    background="white", foreground="black", 
                    borderwidth=1, bordercolor="gray",
                    font=('Helvetica', 12))
    style.map('RoundedButton.TButton',
              background=[('active', '#f0f0f0')])

#Checks to make sure flashcards dir exists
def ensure_flashcards_dir():
    if not os.path.exists(FLASHCARDS_DIR):
        os.makedirs(FLASHCARDS_DIR)

#Function to open uploaded file
def open_file(title="Select a File"):
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(initialdir="./", title=title)
    return file_path

#Function to ask for name of the json file
def get_output_file_name():
    root = Tk()
    root.withdraw()
    while True:
        file_name = simpledialog.askstring("Input", "Enter a name for your flashcard set (without .json):")
        if file_name:
            file_name = file_name.strip()
            if file_name:
                return os.path.join(FLASHCARDS_DIR, f"{file_name}.json")
        print("Please enter a valid name.")

def generate_flashcards(file_path):
    #API token
    client = OpenAI()

    #Initiating ai instructions
    assistant = client.beta.assistants.create(
        name="Study Assistant",
        instructions="""You are an intelligent study assistant designed to help students with their studies.
        Your primary role is to provide information from the study materials provided.""",
        model="gpt-4o",
        tools=[{"type": "file_search"}],
    )

    #Ai reads the uploaded file
    with open(file_path, "rb") as file_stream:
        message_file = client.files.create(
            file=file_stream, purpose="assistants"
        )

    #Thread instructions for ai, similar to initiating the instructions however more specific to the task. Possible modularity
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

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id, assistant_id=assistant.id
    )

    messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
    message_content = messages[0].content[0].text.value

    #Sends the json formatted response to extract_json_objects function
    return extract_json_objects(message_content)

def update_flashcards_json(new_flashcards, output_file):
    try:
        if os.path.exists(output_file):
            with open(output_file, 'r') as json_file:
                existing_flashcards = json.load(json_file)
            existing_flashcards.extend(new_flashcards)
        else:
            existing_flashcards = new_flashcards

        with open(output_file, 'w') as json_file:
            json.dump(existing_flashcards, json_file, indent=4)

        print(f"Total flashcards in {output_file}: {len(existing_flashcards)}")
    except Exception as e:
        print(f"An error occurred while updating the flashcards: {e}")

def get_user_choice():
    root = Tk()
    configure_button_style()
    root.title("Flashcard App")
    
    choice = [None]  # Using a list to store the choice

    def make_choice(value):
        choice[0] = value
        root.quit()

    label = Label(root, text="Do you want to generate a new flashcard set?", font=('Helvetica', 14))
    label.pack(pady=20)

    yes_button = Button(root, text="Yes", command=lambda: make_choice(True), style='RoundedButton.TButton')
    yes_button.pack(side="left", padx=20, pady=20)

    no_button = Button(root, text="No", command=lambda: make_choice(False), style='RoundedButton.TButton')
    no_button.pack(side="right", padx=20, pady=20)

    root.protocol("WM_DELETE_WINDOW", lambda: make_choice(None))
    root.mainloop()

    try:
        root.destroy()  # Attempt to destroy the window after mainloop exits
    except:
        pass  # Ignore any errors that occur during destroy

    return choice[0]

def main():
    ensure_flashcards_dir()
    generate_new = get_user_choice()

    if generate_new:
        # Step 1: Upload file
        file_path = open_file("Select study material")
        if not file_path:
            print("No file selected. Exiting.")
            return

        # Step 2: Generate definitions
        print("Generating flashcards...")
        new_flashcards = generate_flashcards(file_path)

        # Step 3: Get output file name from user
        output_file = get_output_file_name()

        # Step 4: Convert to JSON and update the specified file
        print(f"Updating {output_file}...")
        update_flashcards_json(new_flashcards, output_file)
    else:
        # If not generating new flashcards, just proceed to running the flashcard app
        pass

    # Step 5: Run the flashcard app
    print("Starting flashcard app...")
    run_flashcard_app()

if __name__ == "__main__":
    main()