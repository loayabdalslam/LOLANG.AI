from ai_agent import AIAgent
from terminal_colors import TerminalColors
from config import GeminiConfig
import time
import logging
import os

logging.basicConfig(level=logging.INFO)

def main():
    config = GeminiConfig.get_default_config()
    
    # Initialize agents with different colors
    agent1 = AIAgent("Agent-1", TerminalColors.BLUE, config)
    agent2 = AIAgent("Agent-2", TerminalColors.GREEN, config)

    # Initial conversation topics
    topics = [
        "Tell me about artificial intelligence",
        "What are the implications of AI in healthcare?",
        "How can we ensure AI safety?",
    ]

    for topic in topics:
        # Agent 1 speaks
        response = agent1.chat(topic)
        print(agent1.speak(response))
        time.sleep(2)

        # Agent 2 responds
        response2 = agent2.chat(response)
        print(agent2.speak(response2))
        time.sleep(2)
        print()

if __name__ == "__main__":
    main()
