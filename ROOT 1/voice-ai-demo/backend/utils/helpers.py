from typing import Any, Dict, List

def format_duration(seconds: float) -> str:
    if seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        remaining_seconds = int(seconds % 60)
        return f"{minutes} minutes {remaining_seconds} seconds"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours} hours {minutes} minutes"

def validate_audio_file(file: Any) -> bool:
    allowed_extensions = ['.wav', '.mp3', '.m4a']
    if hasattr(file, 'filename'):
        extension = file.filename.rsplit('.', 1)[1].lower()
        return extension in allowed_extensions
    return False

def extract_keywords(text: str) -> List[str]:
    # Simple keyword extraction logic (can be improved)
    words = text.split()
    keywords = list(set(words))  # Unique keywords
    return keywords

def generate_response_template(data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "status": "success",
        "data": data,
        "message": "Operation completed successfully."
    }

def handle_error(message: str) -> Dict[str, Any]:
    return {
        "status": "error",
        "message": message
    }