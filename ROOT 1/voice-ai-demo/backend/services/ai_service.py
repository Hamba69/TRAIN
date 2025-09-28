import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import re

# Import other services from the same project
from search_service import SearchService
from transcription_service import TranscriptionService
from audio_service import AudioService

# Import database models
from models import Transcription, AudioFile, AIAnalysis

# Import AI libraries with error handling
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("Warning: OpenAI not installed. Install with: pip install openai")

try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("Warning: Transformers not installed. Install with: pip install transformers torch")

class AIService:
    def __init__(self, db_session, model_type="openai", api_key=None):
        """
        Initialize AI Service with integration to other project services
        
        Args:
            db_session: Database session for accessing transcriptions
            model_type: "openai", "huggingface", or "local"
            api_key: API key for external services
        """
        self.db_session = db_session
        self.model_type = model_type
        self.logger = logging.getLogger(__name__)
        
        # Initialize other services from the project
        self.search_service = SearchService(db_session)
        self.transcription_service = None  # Will be set when needed
        self.audio_service = AudioService()
        
        # Initialize the appropriate AI model
        if model_type == "openai":
            if not api_key:
                raise ValueError("OpenAI API key required for OpenAI model")
            openai.api_key = api_key
            self.model = None  # We'll use openai directly
        elif model_type == "huggingface":
            # Initialize Hugging Face transformers
            self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
            self.qa_pipeline = pipeline("question-answering")
            self.model = None
        else:
            # For local/custom models
            self.model = None

    def set_transcription_service(self, transcription_service: TranscriptionService):
        """Set the transcription service for this AI service"""
        self.transcription_service = transcription_service
            
    def process_query(self, query: str, context_recordings: List[str] = None) -> Dict[str, Any]:
        """
        Process a user query against transcribed recordings using SearchService
        
        Args:
            query: User's question or request
            context_recordings: Optional list of specific recording IDs to search
            
        Returns:
            Dict containing response and metadata
        """
        try:
            # Use SearchService to get relevant transcriptions
            if context_recordings:
                # Get specific recordings by ID (assuming SearchService has this method)
                context_transcriptions = []
                for rec_id in context_recordings:
                    # This would need to be implemented in SearchService
                    pass
            else:
                # Use SearchService to find relevant transcriptions
                context_transcriptions = self.search_service.search_transcriptions(query)
            
            context_texts = [trans.text for trans in context_transcriptions[:5]]  # Limit to top 5
            
            if self.model_type == "openai":
                response = self._process_with_openai(query, context_texts)
            elif self.model_type == "huggingface":
                response = self._process_with_huggingface(query, context_texts)
            else:
                response = self._process_with_local_model(query, context_texts)
                
            return {
                "success": True,
                "response": response,
                "query": query,
                "timestamp": datetime.now().isoformat(),
                "context_used": len(context_texts) > 0,
                "sources_found": len(context_transcriptions)
            }
            
        except Exception as e:
            self.logger.error(f"Error processing query: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "query": query,
                "timestamp": datetime.now().isoformat()
            }

    def summarize_recording(self, recording_id: str, summary_type: str = "brief") -> Dict[str, Any]:
        """
        Generate a summary of a specific recording using SearchService to find it
        
        Args:
            recording_id: ID of the recording to summarize
            summary_type: "brief", "detailed", or "bullet_points"
            
        Returns:
            Dict containing summary and metadata
        """
        try:
            # Use SearchService to get the transcription
            # First get all audio files and find the one we want
            audio_files = self.search_service.get_audio_files()
            target_audio_file = None
            
            for audio_file in audio_files:
                if str(audio_file.id) == recording_id or audio_file.filename.contains(recording_id):
                    target_audio_file = audio_file
                    break
            
            if not target_audio_file:
                return {
                    "success": False,
                    "error": f"Recording {recording_id} not found",
                    "recording_id": recording_id
                }
            
            # Get associated transcription
            # This assumes there's a relationship between AudioFile and Transcription
            transcription = self.db_session.query(Transcription).filter(
                Transcription.audio_file_id == target_audio_file.id
            ).first()
            
            if not transcription:
                return {
                    "success": False,
                    "error": f"No transcription found for recording {recording_id}",
                    "recording_id": recording_id
                }
            
            # Generate summary based on model type
            if self.model_type == "openai":
                summary = self._summarize_with_openai(transcription.text, summary_type)
            elif self.model_type == "huggingface":
                summary = self._summarize_with_huggingface(transcription.text, summary_type)
            else:
                summary = self._summarize_with_local_model(transcription.text, summary_type)
                
            return {
                "success": True,
                "summary": summary,
                "recording_id": recording_id,
                "filename": target_audio_file.filename,
                "summary_type": summary_type,
                "original_length": len(transcription.text.split()),
                "summary_length": len(summary.split()),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error summarizing recording {recording_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "recording_id": recording_id
            }

    def extract_information(self, query: str, extraction_type: str = "general") -> Dict[str, Any]:
        """
        Extract specific information from transcriptions using SearchService
        
        Args:
            query: What information to extract
            extraction_type: "general", "names", "dates", "actions", "topics"
            
        Returns:
            Dict containing extracted information
        """
        try:
            # Use SearchService to get relevant transcriptions
            relevant_transcriptions = self.search_service.search_transcriptions(query)
            
            if extraction_type == "names":
                extracted_info = self._extract_names(relevant_transcriptions)
            elif extraction_type == "dates":
                extracted_info = self._extract_dates(relevant_transcriptions)
            elif extraction_type == "actions":
                extracted_info = self._extract_actions(relevant_transcriptions, query)
            elif extraction_type == "topics":
                extracted_info = self._extract_topics(relevant_transcriptions)
            else:
                extracted_info = self._extract_general_info(relevant_transcriptions, query)
                
            return {
                "success": True,
                "extracted_info": extracted_info,
                "extraction_type": extraction_type,
                "query": query,
                "sources_count": len(relevant_transcriptions),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error extracting information: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "query": query
            }

    def analyze_trends(self, time_range: str = "30d", analysis_type: str = "topics") -> Dict[str, Any]:
        """
        Analyze trends in recordings over time using SearchService
        
        Args:
            time_range: "7d", "30d", "90d", "1y"
            analysis_type: "topics", "frequency", "sentiment", "keywords"
            
        Returns:
            Dict containing trend analysis
        """
        try:
            # Parse time range
            days = self._parse_time_range(time_range)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Use SearchService to get transcriptions in time range
            transcriptions = self.search_service.filter_by_date(
                start_date.isoformat(), 
                end_date.isoformat()
            )
            
            if not transcriptions:
                return {
                    "success": True,
                    "trends": [],
                    "message": f"No recordings found in the last {time_range}",
                    "time_range": time_range
                }
            
            # Analyze trends based on type
            if analysis_type == "topics":
                trends = self._analyze_topic_trends(transcriptions)
            elif analysis_type == "frequency":
                trends = self._analyze_frequency_trends(transcriptions)
            elif analysis_type == "sentiment":
                trends = self._analyze_sentiment_trends(transcriptions)
            elif analysis_type == "keywords":
                trends = self._analyze_keyword_trends(transcriptions)
            else:
                trends = self._analyze_general_trends(transcriptions)
                
            return {
                "success": True,
                "trends": trends,
                "analysis_type": analysis_type,
                "time_range": time_range,
                "recordings_analyzed": len(transcriptions),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing trends: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "time_range": time_range
            }

    def transcribe_and_analyze_current_recording(self, transcription_model) -> Dict[str, Any]:
        """
        Integrate with AudioService to transcribe current recording and provide AI analysis
        
        Args:
            transcription_model: Model to use for transcription
            
        Returns:
            Dict containing transcription and AI analysis
        """
        try:
            # Check if AudioService is currently recording
            if not self.audio_service.is_recording:
                return {
                    "success": False,
                    "error": "No active recording found",
                    "message": "Start a recording first using AudioService"
                }
            
            # Stop the current recording and get audio data
            audio_data = self.audio_service.stop_recording()
            
            if not audio_data:
                return {
                    "success": False,
                    "error": "No audio data captured"
                }
            
            # Initialize TranscriptionService if not already done
            if not self.transcription_service:
                self.transcription_service = TranscriptionService(transcription_model)
            
            # Save audio data temporarily and transcribe
            # This would need proper audio file handling
            temp_audio_path = "/tmp/current_recording.wav"  # Simplified
            # Save audio_data to temp_audio_path (implementation needed)
            
            transcribed_text = self.transcription_service.transcribe_audio(temp_audio_path)
            
            # Analyze the transcription
            analysis = self._analyze_fresh_transcription(transcribed_text)
            
            return {
                "success": True,
                "transcription": transcribed_text,
                "analysis": analysis,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error transcribing and analyzing recording: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    def smart_search_with_context(self, query: str, include_audio_context: bool = False) -> Dict[str, Any]:
        """
        Enhanced search that combines SearchService results with AI interpretation
        
        Args:
            query: Search query
            include_audio_context: Whether to include audio file metadata
            
        Returns:
            Enhanced search results with AI insights
        """
        try:
            # Use SearchService for basic search
            transcription_results = self.search_service.search_transcriptions(query)
            
            if include_audio_context:
                audio_results = self.search_service.search_audio_files(query)
            else:
                audio_results = []
            
            # AI-enhanced interpretation of results
            if transcription_results:
                ai_summary = self._generate_search_summary(query, transcription_results)
                suggested_follow_ups = self._generate_follow_up_questions(query, transcription_results)
            else:
                ai_summary = f"No direct matches found for '{query}'. Consider trying related terms."
                suggested_follow_ups = []
            
            return {
                "success": True,
                "query": query,
                "transcription_results": [
                    {
                        "id": trans.id,
                        "text_snippet": trans.text[:200] + "..." if len(trans.text) > 200 else trans.text,
                        "created_at": trans.created_at.isoformat(),
                        "relevance_score": self._calculate_relevance(query, trans.text)
                    }
                    for trans in transcription_results
                ],
                "audio_results": [
                    {
                        "id": audio.id,
                        "filename": audio.filename,
                        "created_at": audio.created_at.isoformat()
                    }
                    for audio in audio_results
                ] if include_audio_context else [],
                "ai_summary": ai_summary,
                "suggested_follow_ups": suggested_follow_ups,
                "total_matches": len(transcription_results),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error in smart search: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "query": query
            }

    # Private helper methods remain largely the same but now use project services
    def _process_with_openai(self, query: str, context: List[str]) -> str:
        """Process query using OpenAI API"""
        context_text = "\n\n".join(context) if context else "No previous recordings found."
        
        prompt = f"""
        Based on the following transcribed recordings from the user's audio files, please answer their question.
        
        Transcribed Content from their recordings:
        {context_text}
        
        User Question: {query}
        
        Please provide a helpful and accurate response based on the transcribed content from their recordings.
        If the transcriptions don't contain relevant information, let them know and suggest they might want to record more content on this topic.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()

    def _process_with_huggingface(self, query: str, context: List[str]) -> str:
        """Process query using Hugging Face models"""
        if not context:
            return "No relevant recordings found to answer your question. Try recording some content about this topic first."
            
        # Use the QA pipeline with the most relevant context
        context_text = context[0]  # Use first context for simplicity
        
        result = self.qa_pipeline(question=query, context=context_text)
        return result['answer']

    def _generate_search_summary(self, query: str, results) -> str:
        """Generate AI summary of search results"""
        if not results:
            return f"No matches found for '{query}'"
        
        # Combine text from top results
        combined_text = " ".join([r.text for r in results[:3]])[:1000]
        
        if self.model_type == "openai":
            prompt = f"Summarize what was found about '{query}' in these recordings: {combined_text}"
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.5
            )
            return response.choices[0].message.content.strip()
        else:
            return f"Found {len(results)} recordings mentioning '{query}'"

    def _generate_follow_up_questions(self, query: str, results) -> List[str]:
        """Generate suggested follow-up questions"""
        if len(results) < 2:
            return []
        
        # Simple keyword extraction for follow-ups
        all_text = " ".join([r.text for r in results[:5]]).lower()
        words = set(all_text.split())
        
        # Filter for meaningful words
        meaningful_words = [w for w in words if len(w) > 4 and w not in ['that', 'this', 'with', 'they', 'were', 'have', 'been']]
        
        if len(meaningful_words) >= 3:
            return [
                f"Tell me more about {meaningful_words[0]}",
                f"What else was mentioned about {meaningful_words[1]}?",
                f"How does {meaningful_words[2]} relate to {query}?"
            ]
        
        return []

    def _calculate_relevance(self, query: str, text: str) -> float:
        """Calculate relevance score between query and text"""
        query_words = set(query.lower().split())
        text_words = set(text.lower().split())
        
        intersection = len(query_words.intersection(text_words))
        union = len(query_words.union(text_words))
        
        return intersection / union if union > 0 else 0.0

    def _analyze_fresh_transcription(self, text: str) -> Dict[str, Any]:
        """Analyze a newly transcribed text"""
        return {
            "word_count": len(text.split()),
            "key_topics": self._extract_topics_from_text(text),
            "estimated_duration": len(text.split()) * 0.5,  # Rough estimate
            "suggested_tags": self._suggest_tags(text)
        }

    def _extract_topics_from_text(self, text: str) -> List[str]:
        """Extract key topics from text"""
        # Simple keyword extraction
        words = text.lower().split()
        word_freq = {}
        
        for word in words:
            if len(word) > 4:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Return top 5 most frequent meaningful words
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:5]]

    def _suggest_tags(self, text: str) -> List[str]:
        """Suggest tags for the transcription"""
        # Simple tag suggestion based on content
        tags = []
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['meeting', 'discussion', 'call']):
            tags.append('meeting')
        if any(word in text_lower for word in ['idea', 'brainstorm', 'think']):
            tags.append('ideas')
        if any(word in text_lower for word in ['todo', 'task', 'need to', 'should']):
            tags.append('tasks')
        if any(word in text_lower for word in ['project', 'work', 'deadline']):
            tags.append('work')
        
        return tags

    # Other helper methods remain similar but now work with the project's data models
    def _parse_time_range(self, time_range: str) -> int:
        """Parse time range string to days"""
        if time_range == "7d":
            return 7
        elif time_range == "30d":
            return 30
        elif time_range == "90d":
            return 90
        elif time_range == "1y":
            return 365
        else:
            return 30  # Default to 30 days

    def _extract_names(self, transcriptions) -> List[str]:
        """Extract person names from transcriptions"""
        names = set()
        name_pattern = r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b'
        
        for trans in transcriptions:
            found_names = re.findall(name_pattern, trans.text)
            names.update(found_names)
            
        return list(names)

    def _extract_dates(self, transcriptions) -> List[str]:
        """Extract dates from transcriptions"""
        dates = set()
        date_patterns = [
            r'\d{1,2}/\d{1,2}/\d{4}',  # MM/DD/YYYY
            r'\d{4}-\d{2}-\d{2}',      # YYYY-MM-DD
            r'[A-Za-z]+ \d{1,2}, \d{4}'  # Month DD, YYYY
        ]
        
        for trans in transcriptions:
            for pattern in date_patterns:
                found_dates = re.findall(pattern, trans.text)
                dates.update(found_dates)
                
        return list(dates)

    def _analyze_topic_trends(self, transcriptions) -> List[Dict[str, Any]]:
        """Analyze topic trends over time"""
        # Simple keyword frequency analysis across all transcriptions
        word_counts = {}
        for trans in transcriptions:
            words = trans.text.lower().split()
            for word in words:
                if len(word) > 3:  # Filter short words
                    word_counts[word] = word_counts.get(word, 0) + 1
        
        # Get top 10 trending topics
        sorted_topics = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return [{"topic": topic, "frequency": freq} for topic, freq in sorted_topics]

    def _analyze_frequency_trends(self, transcriptions) -> Dict[str, Any]:
        """Analyze recording frequency over time"""
        # Group by date
        date_counts = {}
        for trans in transcriptions:
            date_key = trans.created_at.strftime('%Y-%m-%d')
            date_counts[date_key] = date_counts.get(date_key, 0) + 1
            
        return {
            "daily_counts": date_counts,
            "total_recordings": len(transcriptions),
            "average_per_day": len(transcriptions) / len(date_counts) if date_counts else 0
        }

    def _extract_actions(self, transcriptions, query: str) -> List[str]:
        """Extract action items from transcriptions"""
        actions = []
        action_patterns = [
            r'need to \w+',
            r'should \w+',
            r'must \w+',
            r'will \w+',
            r'going to \w+'
        ]
        
        for trans in transcriptions:
            for pattern in action_patterns:
                found_actions = re.findall(pattern, trans.text, re.IGNORECASE)
                actions.extend(found_actions)
        
        return list(set(actions))

    def _extract_topics(self, transcriptions) -> List[str]:
        """Extract topics from transcriptions"""
        return self._analyze_topic_trends(transcriptions)

    def _extract_general_info(self, transcriptions, query: str) -> Dict[str, Any]:
        """Extract general information based on query"""
        return {
            "matching_snippets": [
                trans.text[max(0, trans.text.lower().find(query.lower())-50):
                          trans.text.lower().find(query.lower())+100]
                for trans in transcriptions 
                if query.lower() in trans.text.lower()
            ][:5],
            "total_matches": len(transcriptions),
            "query": query
        }

    def _analyze_sentiment_trends(self, transcriptions) -> List[Dict[str, Any]]:
        """Analyze sentiment trends (simplified)"""
        # Simple sentiment analysis based on keywords
        positive_words = ['good', 'great', 'excellent', 'happy', 'success', 'achieved']
        negative_words = ['bad', 'terrible', 'failed', 'problem', 'issue', 'difficult']
        
        sentiment_over_time = []
        for trans in transcriptions:
            text_lower = trans.text.lower()
            pos_count = sum(1 for word in positive_words if word in text_lower)
            neg_count = sum(1 for word in negative_words if word in text_lower)
            
            sentiment_score = pos_count - neg_count
            sentiment_over_time.append({
                "date": trans.created_at.strftime('%Y-%m-%d'),
                "sentiment_score": sentiment_score,
                "text_preview": trans.text[:100] + "..."
            })
        
        return sentiment_over_time

    def _analyze_keyword_trends(self, transcriptions) -> Dict[str, Any]:
        """Analyze keyword trends over time"""
        return self._analyze_topic_trends(transcriptions)

    def _analyze_general_trends(self, transcriptions) -> Dict[str, Any]:
        """General trend analysis"""
        return {
            "topic_trends": self._analyze_topic_trends(transcriptions),
            "frequency_trends": self._analyze_frequency_trends(transcriptions),
            "total_recordings": len(transcriptions)
        }

    def _summarize_with_local_model(self, text: str, summary_type: str) -> str:
        """Summarize using local model (placeholder)"""
        if summary_type == "brief":
            return f"Brief summary of {len(text.split())} words using local model"
        elif summary_type == "detailed":
            return f"Detailed summary of transcription with {len(text.split())} words"
        else:
            return f"• Key points from transcription\n• Contains {len(text.split())} words\n• Generated using local model"

    def _summarize_with_openai(self, text: str, summary_type: str) -> str:
        """Summarize text using OpenAI"""
        if summary_type == "brief":
            instruction = "Provide a brief 1-2 sentence summary"
        elif summary_type == "detailed":
            instruction = "Provide a detailed summary with key points"
        else:  # bullet_points
            instruction = "Provide a summary in bullet points"
            
        prompt = f"{instruction} of the following transcription from the user's audio recording:\n\n{text}"
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.5
        )
        
        return response.choices[0].message.content.strip()

    def _summarize_with_huggingface(self, text: str, summary_type: str) -> str:
        """Summarize text using Hugging Face"""
        # Truncate if too long for the model
        if len(text) > 1024:
            text = text[:1024]
            
        summary = self.summarizer(text, max_length=150, min_length=30, do_sample=False)
        return summary[0]['summary_text']