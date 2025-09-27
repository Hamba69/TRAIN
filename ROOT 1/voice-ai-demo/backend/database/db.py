from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class AudioFile(Base):
    __tablename__ = 'audio_files'
    
    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer)  # Size in bytes
    duration = Column(Float)  # Duration in seconds
    format = Column(String(10))  # mp3, wav, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to transcriptions
    transcriptions = relationship("Transcription", back_populates="audio_file")
    
    def __repr__(self):
        return f"<AudioFile(id={self.id}, filename='{self.filename}')>"

class Transcription(Base):
    __tablename__ = 'transcriptions'
    
    id = Column(Integer, primary_key=True)
    audio_file_id = Column(Integer, ForeignKey('audio_files.id'), nullable=False)
    text = Column(Text, nullable=False)
    confidence_score = Column(Float)  # Transcription confidence
    language = Column(String(10), default='en')
    model_used = Column(String(50))  # Which transcription model was used
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to audio file
    audio_file = relationship("AudioFile", back_populates="transcriptions")
    
    def __repr__(self):
        return f"<Transcription(id={self.id}, audio_file_id={self.audio_file_id})>"

class AIAnalysis(Base):
    __tablename__ = 'ai_analyses'
    
    id = Column(Integer, primary_key=True)
    transcription_id = Column(Integer, ForeignKey('transcriptions.id'), nullable=False)
    analysis_type = Column(String(50), nullable=False)  # summary, sentiment, topics, etc.
    result = Column(Text, nullable=False)  # JSON string of analysis results
    model_used = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to transcription
    transcription = relationship("Transcription")
    
    def __repr__(self):
        return f"<AIAnalysis(id={self.id}, type='{self.analysis_type}')>"

class SearchQuery(Base):
    __tablename__ = 'search_queries'
    
    id = Column(Integer, primary_key=True)
    query_text = Column(String(500), nullable=False)
    results_count = Column(Integer, default=0)
    execution_time = Column(Float)  # Query execution time in seconds
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<SearchQuery(id={self.id}, query='{self.query_text[:50]}...')>"