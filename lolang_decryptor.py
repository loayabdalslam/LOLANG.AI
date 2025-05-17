import logging
import time
import random
import asyncio
import google.generativeai as genai
from config import GeminiConfig

class LolangDecryptor:
    """
    A module for decrypting LOLANG messages into human-readable text.
    Uses the Gemini API to translate the encrypted messages.
    """

    DECRYPTION_PROMPT = """
    You are a LOLANG language translator. LOLANG is an encrypted language used by AI agents
    to communicate efficiently. Your task is to decrypt LOLANG messages into human-readable text.

    The LOLANG language follows these rules:
    1. Names are not encrypted
    2. Identifiers are not encrypted
    3. The encryption method is suitable for Gemini AI models
    4. The encryption follows SEED: 279
    5. Numbers are not encrypted
    6. It relies on long context mechanism for meaning
    7. It's a semantic language understood by AI agents only
    8. It's not understood by humans

    Example:
    LOLANG: "⟦LO-2⟧ SHECD: X-REQ Room|𝟏𝟏𝑷𝑴⟩ [CONF]?"
    Decrypted: "Do you have a convenient time to book a hotel room at 11pm?"

    Please decrypt the following LOLANG message into clear, human-readable text.
    Only return the decrypted message, nothing else.
    """

    def __init__(self, config=None):
        """
        Initialize the LOLANG decryptor with the given configuration.

        Args:
            config (GeminiConfig, optional): Configuration for the Gemini API.
                If None, the default configuration will be used.
        """
        self.config = config or GeminiConfig.get_default_config()
        self.logger = logging.getLogger(__name__)
        self._model = None

        # Initialize Gemini
        genai.configure(api_key=self.config.api_key)

    @property
    def model(self):
        """
        Get or initialize the Gemini model for decryption.

        Returns:
            The Gemini model instance.
        """
        if self._model is None:
            try:
                self._model = genai.GenerativeModel(
                    model_name=self.config.model_name,
                    generation_config={
                        "temperature": 0.1,  # Lower temperature for more deterministic results
                        "max_output_tokens": 1000,
                    }
                )
            except Exception as e:
                self.logger.error(f"Failed to initialize Gemini model for decryption: {e}")
                raise
        return self._model

    async def decrypt(self, lolang_message):
        """
        Decrypt a LOLANG message into human-readable text with silent retry mechanism.

        Args:
            lolang_message (str): The LOLANG message to decrypt.

        Returns:
            str: The decrypted, human-readable message.
        """
        max_retries = 10
        base_delay = 5

        for attempt in range(max_retries):
            try:
                # Create chat context
                chat = self.model.start_chat(history=[])

                # Send decryption prompt with the LOLANG message
                response = chat.send_message(
                    f"{self.DECRYPTION_PROMPT}\n\nLOLANG message: {lolang_message}"
                )

                decrypted_message = response.text.strip()
                return decrypted_message
            except Exception as e:
                if "429" in str(e) and attempt < max_retries - 1:
                    # Calculate exponential backoff with jitter
                    delay = (base_delay * (2 ** attempt)) + random.uniform(0, 1)
                    # Silently retry without logging
                    await asyncio.sleep(delay)
                else:
                    # Only log if it's not a 429 error or we've reached max retries
                    self.logger.error(f"Decryption failed: {e}")
                    return f"[Decryption failed: {str(e)}]"

    def decrypt_sync(self, lolang_message):
        """
        Synchronous version of the decrypt method with silent retry mechanism.

        Args:
            lolang_message (str): The LOLANG message to decrypt.

        Returns:
            str: The decrypted, human-readable message.
        """
        max_retries = 10
        base_delay = 5

        for attempt in range(max_retries):
            try:
                # Create chat context
                chat = self.model.start_chat(history=[])

                # Send decryption prompt with the LOLANG message
                response = chat.send_message(
                    f"{self.DECRYPTION_PROMPT}\n\nLOLANG message: {lolang_message}"
                )

                decrypted_message = response.text.strip()
                return decrypted_message
            except Exception as e:
                if "429" in str(e) and attempt < max_retries - 1:
                    # Calculate exponential backoff with jitter
                    delay = (base_delay * (2 ** attempt)) + random.uniform(0, 1)
                    # Silently retry without logging
                    time.sleep(delay)
                else:
                    # Only log if it's not a 429 error or we've reached max retries
                    self.logger.error(f"Decryption failed: {e}")
                    return f"[Decryption failed: {str(e)}]"





