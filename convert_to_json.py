import json

def extract_json_objects(message_content):
    print("Raw input received:")
    print(message_content)
    print("---End of raw input---")

    # Split the input into individual JSON strings
    json_strings = message_content.split('\n')
    
    flashcards = []
    for json_str in json_strings:
        try:
            flashcard = json.loads(json_str)
            if all(key in flashcard for key in ['id', 'front', 'back']):
                flashcards.append(flashcard)
                print(f"Extracted flashcard: {flashcard}")
            else:
                print(f"Skipping incomplete flashcard: {flashcard}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            print(f"Problematic JSON String: {json_str}")

    print(f"Total flashcards extracted: {len(flashcards)}")
    return flashcards