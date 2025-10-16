"""
Text-to-Speech service for multi-language support.
"""
import os
import asyncio
from typing import Optional
from gtts import gTTS
import pyttsx3
from pathlib import Path
import uuid
from datetime import datetime

from app.core.config import settings


class TTSService:
    """Text-to-Speech service supporting multiple languages."""
    
    # Language codes mapping
    LANGUAGE_CODES = {
        'en': 'en',      # English
        'hi': 'hi',      # Hindi
        'te': 'te',      # Telugu
        'ta': 'ta',      # Tamil
        'bn': 'bn',      # Bengali
        'gu': 'gu',      # Gujarati
        'kn': 'kn',      # Kannada
        'ml': 'ml',      # Malayalam
        'mr': 'mr',      # Marathi
        'pa': 'pa',      # Punjabi
        'or': 'or'       # Odia
    }
    
    # Voice settings for different languages
    VOICE_SETTINGS = {
        'en': {
            'engine': 'gtts',
            'voice_id': 'en-us',
            'rate': 150,
            'volume': 0.8
        },
        'hi': {
            'engine': 'gtts',
            'voice_id': 'hi-in',
            'rate': 140,
            'volume': 0.8
        },
        'te': {
            'engine': 'gtts',
            'voice_id': 'te-in',
            'rate': 140,
            'volume': 0.8
        },
        'ta': {
            'engine': 'gtts',
            'voice_id': 'ta-in',
            'rate': 140,
            'volume': 0.8
        }
    }
    
    def __init__(self):
        """Initialize TTS service."""
        self.output_dir = Path(settings.upload_dir) / "voice"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize pyttsx3 engine for offline TTS
        try:
            self.offline_engine = pyttsx3.init()
            self._configure_offline_engine()
        except Exception as e:
            print(f"Failed to initialize offline TTS engine: {e}")
            self.offline_engine = None
    
    def _configure_offline_engine(self):
        """Configure offline TTS engine."""
        if self.offline_engine:
            # Set properties
            voices = self.offline_engine.getProperty('voices')
            
            # Try to set a female voice if available
            for voice in voices:
                if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                    self.offline_engine.setProperty('voice', voice.id)
                    break
            
            self.offline_engine.setProperty('rate', 150)
            self.offline_engine.setProperty('volume', 0.8)
    
    async def generate_voice(
        self, 
        text: str, 
        language: str = 'en', 
        user_id: Optional[int] = None
    ) -> Optional[str]:
        """
        Generate voice file from text.
        
        Args:
            text: Text to convert to speech
            language: Language code
            user_id: User ID for file naming
            
        Returns:
            Path to generated voice file or None if failed
        """
        try:
            # Validate language
            if language not in self.LANGUAGE_CODES:
                language = 'en'  # Default to English
            
            # Clean and prepare text
            cleaned_text = self._clean_text(text)
            if not cleaned_text:
                return None
            
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"voice_{user_id or 'anon'}_{timestamp}_{uuid.uuid4().hex[:8]}.mp3"
            file_path = self.output_dir / filename
            
            # Get voice settings
            voice_settings = self.VOICE_SETTINGS.get(language, self.VOICE_SETTINGS['en'])
            
            # Generate voice file
            if voice_settings['engine'] == 'gtts':
                success = await self._generate_with_gtts(
                    text=cleaned_text,
                    language=language,
                    file_path=file_path
                )
            else:
                success = await self._generate_with_offline(
                    text=cleaned_text,
                    language=language,
                    file_path=file_path,
                    settings=voice_settings
                )
            
            if success and file_path.exists():
                return str(file_path)
            
            return None
            
        except Exception as e:
            print(f"Error generating voice: {e}")
            return None
    
    async def _generate_with_gtts(
        self, 
        text: str, 
        language: str, 
        file_path: Path
    ) -> bool:
        """Generate voice using Google Text-to-Speech."""
        try:
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            success = await loop.run_in_executor(
                None, 
                self._gtts_sync_generate, 
                text, 
                language, 
                file_path
            )
            return success
        except Exception as e:
            print(f"gTTS generation failed: {e}")
            return False
    
    def _gtts_sync_generate(self, text: str, language: str, file_path: Path) -> bool:
        """Synchronous gTTS generation."""
        try:
            # Get language code
            lang_code = self.LANGUAGE_CODES.get(language, 'en')
            
            # Create TTS object
            tts = gTTS(text=text, lang=lang_code, slow=False)
            
            # Save to file
            tts.save(str(file_path))
            
            return True
        except Exception as e:
            print(f"gTTS sync generation failed: {e}")
            return False
    
    async def _generate_with_offline(
        self, 
        text: str, 
        language: str, 
        file_path: Path,
        settings: dict
    ) -> bool:
        """Generate voice using offline TTS engine."""
        try:
            if not self.offline_engine:
                return False
            
            # Run in thread pool
            loop = asyncio.get_event_loop()
            success = await loop.run_in_executor(
                None,
                self._offline_sync_generate,
                text,
                file_path,
                settings
            )
            return success
        except Exception as e:
            print(f"Offline TTS generation failed: {e}")
            return False
    
    def _offline_sync_generate(self, text: str, file_path: Path, settings: dict) -> bool:
        """Synchronous offline TTS generation."""
        try:
            # Set properties
            self.offline_engine.setProperty('rate', settings.get('rate', 150))
            self.offline_engine.setProperty('volume', settings.get('volume', 0.8))
            
            # Save to file
            self.offline_engine.save_to_file(text, str(file_path))
            self.offline_engine.runAndWait()
            
            return True
        except Exception as e:
            print(f"Offline sync generation failed: {e}")
            return False
    
    def _clean_text(self, text: str) -> str:
        """Clean and prepare text for TTS."""
        if not text:
            return ""
        
        # Remove excessive whitespace
        cleaned = ' '.join(text.split())
        
        # Remove special characters that might cause issues
        cleaned = cleaned.replace('*', '').replace('#', '').replace('_', '')
        
        # Limit text length (most TTS services have limits)
        if len(cleaned) > 1000:
            cleaned = cleaned[:1000] + "..."
        
        return cleaned
    
    def get_available_languages(self) -> list:
        """Get list of available languages."""
        return list(self.LANGUAGE_CODES.keys())
    
    def get_voice_info(self, language: str) -> dict:
        """Get voice information for a language."""
        return self.VOICE_SETTINGS.get(language, self.VOICE_SETTINGS['en'])
    
    def delete_old_voice_files(self, days_old: int = 7):
        """Delete voice files older than specified days."""
        try:
            import time
            current_time = time.time()
            cutoff_time = current_time - (days_old * 24 * 60 * 60)
            
            deleted_count = 0
            for file_path in self.output_dir.glob("*.mp3"):
                if file_path.stat().st_mtime < cutoff_time:
                    file_path.unlink()
                    deleted_count += 1
            
            print(f"Deleted {deleted_count} old voice files")
            return deleted_count
            
        except Exception as e:
            print(f"Error deleting old voice files: {e}")
            return 0


# Global TTS service instance
tts_service = TTSService()
