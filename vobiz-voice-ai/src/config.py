"""
Application Configuration
Loads environment variables and provides type-safe settings
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Application Settings
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    
    # Vobiz Telephony
    VOBIZ_API_KEY: str
    VOBIZ_SIP_DOMAIN: str = "sip.vobiz.ai"
    VOBIZ_SIP_USERNAME: str
    VOBIZ_SIP_PASSWORD: str
    VOBIZ_WEBHOOK_SECRET: str
    
    # Google Gemini AI
    GOOGLE_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.5-flash-preview-05-20"
    GEMINI_VOICE_ID: str = "en-US-Standard-A"
    GEMINI_LANGUAGE_CODE: str = "en-IN"
    
    # Supabase Database
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_ROLE_KEY: str
    
    # n8n Automation
    N8N_WEBHOOK_URL: str = "http://localhost:5678/webhook/post-call"
    N8N_AUTH_HEADER: Optional[str] = None
    
    # Business Defaults (Dental Clinic)
    DEFAULT_BUSINESS_TYPE: str = "dental_clinic"
    DEFAULT_LANGUAGES: str = "en-IN,hi-IN"
    DEFAULT_TIMEZONE: str = "Asia/Kolkata"
    ESCALATION_PHONE: str
    
    @property
    def languages_list(self) -> List[str]:
        return [lang.strip() for lang in self.DEFAULT_LANGUAGES.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()
