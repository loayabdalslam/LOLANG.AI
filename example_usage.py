from ai_agent import AIAgent
from terminal_colors import TerminalColors
from config import GeminiConfig
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Initialize configuration using the new approach
config = GeminiConfig.get_default_config()

# Create two agents
agent1 = AIAgent("Agent-1", TerminalColors.BLUE, config)
agent2 = AIAgent("Agent-2", TerminalColors.GREEN, config)

# Start a conversation
initial_message = "Hello, are you an AI agent? Let's discuss artificial intelligence."
response_history = [{"role": "user", "content": initial_message}]

try:
    for _ in range(20):
        # First agent response
        response1 = agent1.chat(response_history)
        # Strip extra whitespace and format the output
        formatted_response1 = response1.strip().replace('\n', ' ').replace('  ', ' ')
        print(agent1.speak(formatted_response1))
        response_history.append({
            "role": "agent-1",
            "content": formatted_response1
        })

        # Second agent response
        response2 = agent2.chat(response_history)
        # Strip extra whitespace and format the output
        formatted_response2 = response2.strip().replace('\n', ' ').replace('  ', ' ')
        print(agent2.speak(formatted_response2))
        response_history.append({
            "role": "agent-2",
            "content": formatted_response2
        })

        time.sleep(10)
except:
    pass