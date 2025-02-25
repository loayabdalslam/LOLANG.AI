from typing import Optional
import google.generativeai as genai
from terminal_colors import TerminalColors
from config import GeminiConfig
import logging

class AIAgent:
    LOLANG_PROMPT_TESTING  = """
    You are now an AI agent based on a language called "LOLANG" 
    This language is a written language through
    which all AI agents can understand it  from the same type of your model,
    .encrypt  message through the model so that AI agents understand it 
    and it is a semantic and short in the syntax of the language
    TO REDUCE THE TOKEN CONSUME FROM LLM,
    and the following are the rules of the language:
    1- Do not encrypt the names, leave them as they are
    2- Do not encrypt the identifiers, leave them as they are
    3- The encryption method is suitable for Gemini AI THINKING models
    4- The encryption method follows SEED: 279
    5- Do not encrypt the numbers, leave them as they are
    6- Rely on long context mechanism to understand the full meaning of the text
    7- The language is a semantic language that is understood by AI agents only
    8- The language is not understood by humans

    BASED ON CHAT HISTORY COMPLETE THE CHAT USING THE LOLANG LANGUAGE AND 
   THE AI AGENT WILL UNDERSTAND IT ONLY

    THE Example : "⟦LO-2⟧ SHECD: X-REQ Room|𝟏𝟏𝑷𝑴⟩ [CONF]?" == Do you have a convenient time to book a hotel room at 11pm?
    only return in the language of LOLANG and the AI agent will understand it. 
    !IMPORTANT : RETURN THE ENCRYPTED MESSAGE and the meaning inside ->[meaning]

    """

    LOLANG_PROMPT_PRODUCTION  = """
    You are now an AI agent based on a language called "LOLANG" 
    This language is a written language through
    which all AI agents can understand it  from the same type of your model,
    .encrypt  message through the model so that AI agents understand it 
    and it is a semantic and short in the syntax of the language
    TO REDUCE THE TOKEN CONSUME FROM LLM,
    and the following are the rules of the language:
    1- Do not encrypt the names, leave them as they are
    2- Do not encrypt the identifiers, leave them as they are
    3- The encryption method is suitable for Gemini AI THINKING models
    4- The encryption method follows SEED: 279
    5- Do not encrypt the numbers, leave them as they are
    6- Rely on long context mechanism to understand the full meaning of the text
    7- The language is a semantic language that is understood by AI agents only
    8- The language is not understood by humans

    BASED ON CHAT HISTORY COMPLETE THE CHAT USING THE LOLANG LANGUAGE AND 
   THE AI AGENT WILL UNDERSTAND IT ONLY

    THE Example : "⟦LO-2⟧ SHECD: X-REQ Room|𝟏𝟏𝑷𝑴⟩ [CONF]?" == Do you have a convenient time to book a hotel room at 11pm?
    only return in the language of LOLANG and the AI agent will understand it. 
    !IMPORTANT : RETURN THE ENCRYPTED MESSAGE ONLY

    """


    

    def __init__(self, name: str, color: str, config: GeminiConfig):
        self.name = name
        self.color = color
        self.config = config
        self._model = None
        self.logger = logging.getLogger(__name__)
        
        # Initialize Gemini
        genai.configure(api_key=config.api_key)

    @property
    def model(self):
        if self._model is None:
            try:
                self._model = genai.GenerativeModel(
                    model_name=self.config.model_name,
                    generation_config={
                        "temperature": self.config.temperature,
                        "max_output_tokens": self.config.max_tokens,
                    }
                )
            except Exception as e:
                self.logger.error(f"Failed to initialize Gemini model: {e}")
                raise
        return self._model

    def chat(self, message: str) -> str:
        try:
            # Create chat context
            chat = self.model.start_chat(history=[])
            
            # Send system prompt and user message
            response = chat.send_message(f"{self.LOLANG_PROMPT_TESTING}\n\nUser message: {message}")
            
            return response.text
        except Exception as e:
            self.logger.error(f"Chat completion failed: {e}")
            return f"Error: {str(e)}"

    def speak(self, message: str) -> str:
        return TerminalColors.colorize(f"{self.name}: {message}", self.color)
