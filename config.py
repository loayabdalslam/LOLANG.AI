from dataclasses import dataclass

@dataclass
class GeminiConfig:
    # Default configurations
    api_key: str = "AIzaSyD3DIAlu69Amj0o6UKm3fhORJ3HGOdAEik"
    model_name: str = "gemini-2.0-flash-exp"
    temperature: float = 0.8
    max_tokens: int = 8000

    @classmethod
    def get_default_config(cls) -> 'GeminiConfig':
        return cls()