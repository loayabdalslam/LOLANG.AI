from dataclasses import dataclass

@dataclass
class GeminiConfig:
    # Default configurations
    api_key: str = "AIzaSyD3DIAlu69Amj"
    model_name: str = "gemini-2.0-flash"
    temperature: float = 0.8
    max_tokens: int = 8000

    @classmethod
    def get_default_config(cls) -> 'GeminiConfig':
        return cls()