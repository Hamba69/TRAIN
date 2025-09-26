# Voice AI Demo

## Overview
The Voice AI Demo project is a comprehensive application that integrates voice recording, transcription, and AI-powered responses. It allows users to record audio, transcribe it into text, and interact with an AI system for various functionalities.

## Features
- **Audio Recording**: Users can record audio directly from the application.
- **Transcription**: Recorded audio is transcribed into text for easy access and searching.
- **AI Interaction**: Users can ask questions and receive AI-generated responses based on the transcriptions.
- **Search Functionality**: Users can search through transcriptions and audio files to find specific content.

## Project Structure
```
voice-ai-demo
├── backend
│   ├── app.py
│   ├── models
│   │   └── __init__.py
│   ├── services
│   │   ├── audio_service.py
│   │   ├── transcription_service.py
│   │   ├── ai_service.py
│   │   └── search_service.py
│   ├── database
│   │   └── db.py
│   ├── utils
│   │   └── helpers.py
│   └── requirements.txt
├── frontend
│   ├── src
│   │   ├── App.tsx
│   │   ├── components
│   │   │   ├── VoiceRecorder.tsx
│   │   │   ├── ChatInterface.tsx
│   │   │   └── AudioPlayer.tsx
│   │   ├── api
│   │   │   └── index.ts
│   │   └── index.tsx
│   ├── public
│   │   └── index.html
│   ├── package.json
│   └── tsconfig.json
├── README.md
```

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/voice-ai-demo.git
   cd voice-ai-demo
   ```

2. Navigate to the backend directory and install the required packages:
   ```
   cd backend
   pip install -r requirements.txt
   ```

3. Navigate to the frontend directory and install the required packages:
   ```
   cd ../frontend
   npm install
   ```

## Usage
1. Start the backend server:
   ```
   cd backend
   python app.py
   ```

2. Start the frontend application:
   ```
   cd frontend
   npm start
   ```

3. Open your browser and navigate to `http://localhost:3000` to access the application.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.