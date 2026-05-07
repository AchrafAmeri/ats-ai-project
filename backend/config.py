import sys
from pydantic import SecretStr, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GEMINI_API_KEY: SecretStr

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

try:
    settings = Settings()
except ValidationError:
    # Option: Renvoyer une erreur explicite si la clé est manquante
    raise ValueError("Configuration Error: The 'GEMINI_API_KEY' environment variable is required but was not found.")
except Exception as e:
    # Cas de secours : Valeur par défaut vide si nécessaire pour éviter le crash immédiat
    class FallbackSettings:
        GEMINI_API_KEY = SecretStr("")
    settings = FallbackSettings()