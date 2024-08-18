import os
from openai import OpenAI
from tkinter import Tk, filedialog

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
            When asked to generate a flashcard, please output the information in the following JSON format:

            {
            "id": "", // Leave this field empty; it will be filled in later.
            "front": "<The question, prompt, or term to be placed on the front of the flashcard>",
            "back": "<The answer, explanation, or definition to be placed on the back of the flashcard>",
            }

            Please ensure that the "id" field is left empty (as an empty string) and that the content for "front" and "back" fields is filled in appropriately.""",
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

message_content = messages[0].content[0].text
print(f"Response: \n{message_content.value}\n")