from flask import Flask, request, jsonify
from services.audio_service import AudioService
from services.transcription_service import TranscriptionService
from services.ai_service import AIService
from services.search_service import SearchService

app = Flask(__name__)

# Initialize services
audio_service = AudioService()
transcription_service = TranscriptionService()
ai_service = AIService()
search_service = SearchService()

@app.route('/api/record', methods=['POST'])
def record_audio():
    audio_data = request.json.get('audio_data')
    audio_service.save_audio(audio_data)
    return jsonify({"message": "Audio recorded successfully."}), 201

@app.route('/api/transcribe', methods=['POST'])
def transcribe_audio():
    audio_file = request.files['file']
    transcription = transcription_service.transcribe(audio_file)
    return jsonify({"transcription": transcription}), 200

@app.route('/api/query', methods=['POST'])
def query_ai():
    user_query = request.json.get('query')
    response = ai_service.process_query(user_query)
    return jsonify({"response": response}), 200

@app.route('/api/search', methods=['GET'])
def search_transcriptions():
    query = request.args.get('query')
    results = search_service.search(query)
    return jsonify({"results": results}), 200

if __name__ == '__main__':
    app.run(debug=True)