from dataclasses import dataclass

@dataclass
class GeminiConfig:
    # Default configurations
    api_key: str = "AIzaSyDO0m1er-"
    model_name: str = "gemini-2.0-flash"
    temperature: float = 0.8
    max_tokens: int = 8000
    message_delay: int = 5  # Delay in seconds between messages

    @classmethod
    def get_default_config(cls) -> 'GeminiConfig':
        return cls()
