from flask import jsonify
from typing import Dict, Any

class AIService:
    def __init__(self, ai_model):
        self.ai_model = ai_model

    def process_query(self, query: str) -> Dict[str, Any]:
        response = self.ai_model.generate_response(query)
        return jsonify({"response": response})

    def summarize_recording(self, recording_id: str) -> Dict[str, Any]:
        summary = self.ai_model.summarize(recording_id)
        return jsonify({"summary": summary})

    def extract_information(self, query: str) -> Dict[str, Any]:
        extracted_info = self.ai_model.extract_info(query)
        return jsonify({"extracted_info": extracted_info})

    def analyze_trends(self, time_range: str) -> Dict[str, Any]:
        trends = self.ai_model.analyze_trends(time_range)
        return jsonify({"trends": trends})