import os
import json
from openai import OpenAI
from tkinter import Tk, filedialog
from convert_to_json import extract_json_objects

# Upload file and get file path
def open_file():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(initialdir="C:/", title="Select a File")
    return file_path

file_name = open_file()

client = OpenAI()

assistant = client.beta.assistants.create(
    name="Study Assistant",
    instructions="""You are an intelligent study assistant designed to help students with their studies.
    Your primary role is to provide information from the study materials provided.""",
    model="gpt-4o",
    tools=[{"type": "file_search"}],
)

print(assistant)

# Open the file and upload it, keeping a reference to the file stream
file_stream = open(file_name, "rb")
message_file = client.files.create(
    file=file_stream, purpose="assistants"
)

# Close the file stream properly
file_stream.close()

# Create the thread with the file attached
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

print(thread.tool_resources.file_search)

# Run the assistant and get the response
run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id, assistant_id=assistant.id
)

# Get the messages from the thread and run
messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

message_content = messages[0].content[0].text.value  # Extract the value from the Text object
print(f"Type of message_content: {type(message_content)}")
print(message_content)

flashcards = extract_json_objects(message_content)

output_file = "flashcards.json"

# Read existing flashcards
try:
    with open(output_file, 'r') as json_file:
        existing_flashcards = json.load(json_file)
except (FileNotFoundError, json.JSONDecodeError):
    existing_flashcards = []

# Append new flashcards
existing_flashcards.extend(flashcards)

# Write updated flashcards back to file
with open(output_file, 'w') as json_file:
    json.dump(existing_flashcards, json_file, indent=4)

print(f"Total flashcards in file after update: {len(existing_flashcards)}")