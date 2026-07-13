# The Memory Vault - Stateful AI Chatbot

## Project Overview

The Memory Vault is a state-of-the-art, stateful AI chatbot designed to maintain conversation context across user interactions. Unlike stateless chatbots that forget prior interactions upon page reload or new message generation, The Memory Vault utilizes Streamlit's Session State to remember previous messages, providing a seamless and continuous conversational experience. It integrates seamlessly with the Groq API for lightning-fast and highly intelligent responses.

## Features

- **Stateful Memory**: Persists conversation history using Streamlit Session State, meaning no messages disappear.
- **Multiple AI Personalities**: Includes selectable system prompts via the sidebar (Helpful Assistant, Friendly, Professional, Teacher, Funny).
- **Adjustable Temperature**: Users can fine-tune the creativity of the model using a slider.
- **Modern User Interface**: Employs Streamlit chat input, chat messages, and styling for a professional aesthetic.
- **Resilient Error Handling**: Gracefully handles missing API keys, network connection errors, API failures, and empty responses.
- **Clear Chat Capability**: Easily clear the conversation history with a dedicated sidebar button.

## Screenshots
[Placeholder for application screenshot - add your screenshot to the assets folder and link here]

## Installation

Follow these steps to set up the project locally.

### Virtual Environment Setup

1. Clone or download the repository.
2. Navigate to the project directory:
   ```bash
   cd "Ass-3 The Memory Vault - Stateful AI Chatbot"
   ```
3. Create a Python virtual environment:
   ```bash
   python3 -m venv venv
   ```
4. Activate the virtual environment:
   - On macOS/Linux: source venv/bin/activate
   - On Windows: venv\Scripts\activate

5. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Groq API Setup & Environment Variables

1. Create an account and obtain an API key from the [Groq Console](https://console.groq.com/).
2. Create a file named .env in the root of the project directory (use .env.example as a template).
3. Add your Groq API key to the .env file:
   ```text
   GROQ_API_KEY=your_api_key_here
   ```

### Running the App

Once everything is set up, start the Streamlit application by running:
```bash
streamlit run app.py
```
This will launch a web browser window pointing to the locally hosted application.

## Project Structure

```text
Memory-Vault-Chatbot/
|
|-- app.py             # Main Streamlit application file
|-- requirements.txt   # Python dependencies
|-- .env.example       # Example environment variables file
|-- README.md          # Project documentation
|-- .gitignore         # Files and directories ignored by Git
|-- assets/            # Directory for images and media assets
```

## Technologies Used

- **Python 3.11+**: The core programming language.
- **Streamlit**: A Python framework for building interactive web applications quickly.
- **Groq API**: To access the llama-3.3-70b-versatile language model.
- **python-dotenv**: For managing environment variables securely.

## Assignment Objectives Completed

1. Transitioned from text inputs to a modern chat UI utilizing Streamlit Session State.
2. Implemented comprehensive exception and error handling mechanisms.
3. Designed an interactive sidebar with temperature and personality adjustments.
4. Maintained a clear, professional codebase with modular and well-commented functions compliant with PEP 8.
5. Successfully connected and streamed contexts securely via the Groq API integration.

## Future Improvements

- Add user authentication to allow multiple distinct user sessions and profiles.
- Implement a backend database (like PostgreSQL or MongoDB) for persistent long-term storage of conversations.
- Introduce capability for users to upload documents for context-aware responses (RAG).
- Support for voice input and text-to-speech output.

## License

This project is created for educational purposes and internship assignment completion.
