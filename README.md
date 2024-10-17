# Flashcard Application

This Flashcard Application is a powerful study tool that combines AI-generated flashcards with an interactive GUI for efficient learning. It allows users to create flashcards from study materials and review them in an engaging interface.

## Features

- **AI-Powered Flashcard Generation**: Utilizes OpenAI's GPT-4 to create flashcards from your study materials.
- **Interactive GUI**: User-friendly interface for reviewing flashcards.
- **Flashcard Set Management**: Create, save, and load multiple flashcard sets.
- **Review Mode**: Focus on cards marked as "Don't Know" for targeted studying.
- **Progress Tracking**: Keep track of known and unknown cards throughout your study session.

## Requirements

- Python 3.7+
- OpenAI API key
- Required Python packages (install via `pip install -r requirements.txt`):
  - openai
  - tkinter (usually comes pre-installed with Python)

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/flashcard-application.git
   cd flashcard-application
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   - Create a `.env` file in the project root.
   - Add your OpenAI API key: `OPENAI_API_KEY=your_api_key_here`

## Usage

Run the main application:

```
python main.py
```

### Generating New Flashcards

1. Choose "Generate New Flashcards" when prompted.
2. Select your study material file when the file dialog opens.
3. Wait for the AI to generate flashcards from your material.
4. Enter a name for your new flashcard set when prompted.

### Reviewing Flashcards

1. Choose "Use Existing Flashcards" when prompted.
2. Select a flashcard set file (.json) when the file dialog opens.
3. Use the GUI to review your flashcards:
   - Click the card to flip between front and back.
   - Use "Know" and "Don't Know" buttons to track your progress.
   - Use "Review Unknown" to focus on challenging cards.
   - Use "Change Set" to switch to a different flashcard set.

## Project Structure

- `main.py`: The main entry point of the application.
- `flashcard_gui.py`: Contains the GUI implementation for the flashcard review system.
- `convert_to_json.py`: Handles the conversion of AI-generated content to JSON format.
- `flashcards/`: Directory where flashcard sets are stored as JSON files.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
