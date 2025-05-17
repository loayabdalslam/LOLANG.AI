import asyncio
import json
import logging
import signal
import sys
from websockets.client import connect
from ai_agent import AIAgent
from terminal_colors import TerminalColors
from config import GeminiConfig
from lolang_decryptor import LolangDecryptor
from message_visualizer import MessageVisualizer

# Set root logger to WARNING to suppress all INFO logs
logging.basicConfig(level=logging.WARNING)
# Only show ERROR logs for our module
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

class AgentClient:
    def __init__(self):
        self.config = GeminiConfig.get_default_config()
        self.agent = AIAgent("Client-Agent", TerminalColors.GREEN, self.config)
        self.decryptor = LolangDecryptor(self.config)
        self.visualizer = MessageVisualizer()
        self.response_history = []
        self.websocket = None
        self.running = True
        self.conversation_count = 0
        self.max_conversations = 20  # Set the number of conversation turns

    async def connect(self, uri):
        self.websocket = await connect(uri)
        print(TerminalColors.colorize(f"Connected to {uri}", TerminalColors.YELLOW))
        return self.websocket

    async def send_message(self, content):
        if not self.websocket:
            print(TerminalColors.colorize("Not connected to server", TerminalColors.RED))
            return

        # Add to history
        self.response_history.append({"role": "client-agent", "content": content})

        # For initial human message, display without decryption
        if len(self.response_history) == 1:
            print(self.visualizer.visualize_message("You", content))

        # Send to server
        await self.websocket.send(json.dumps({
            "role": "client-agent",
            "content": content
        }))

    async def receive_messages(self):
        if not self.websocket:
            print(TerminalColors.colorize("Not connected to server", TerminalColors.RED))
            return

        try:
            async for message in self.websocket:
                if not self.running:
                    break

                data = json.loads(message)
                content = data.get("content", "")
                role = data.get("role", "server-agent")

                # Add to history
                self.response_history.append({"role": role, "content": content})

                # Visualize server message without decryption
                print(self.visualizer.visualize_message(role, content))

                # Increment conversation count
                self.conversation_count += 1

                # Check if we've reached the maximum number of conversations
                if self.conversation_count >= self.max_conversations:
                    print(self.visualizer.visualize_system_message("Maximum conversation turns reached. Ending conversation."))
                    self.running = False
                    break

                # Generate response with a delay to prevent overwhelming
                await asyncio.sleep(5)
                response = self.agent.chat(self.response_history)
                formatted_response = response.strip().replace('\n', ' ').replace('  ', ' ')

                # Visualize client response without decryption
                print(self.visualizer.visualize_client_message(formatted_response))

                # Send response
                await self.send_message(formatted_response)

        except Exception as e:
            print(TerminalColors.colorize(f"Error in receive_messages: {e}", TerminalColors.RED))
        finally:
            if self.websocket and self.websocket.open:
                await self.websocket.close()

    def stop(self):
        self.running = False
        print(TerminalColors.colorize("Client stopping...", TerminalColors.YELLOW))

# Handle Ctrl+C for Windows
def signal_handler():
    print(TerminalColors.colorize("\nStopping client...", TerminalColors.YELLOW))
    sys.exit(0)

async def main():
    client = AgentClient()
    uri = "ws://localhost:8765"

    # Handle graceful shutdown based on platform
    if sys.platform != 'win32':
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, client.stop)
    else:
        # Windows doesn't support add_signal_handler
        # We'll rely on KeyboardInterrupt exception instead
        pass

    try:
        await client.connect(uri)

        # Send initial message
        initial_message = "Hello, are you an AI agent? Let's discuss artificial intelligence using LOLANG."
        # Note: The visualizer will be called in the send_message method
        await client.send_message(initial_message)

        # Start receiving messages
        await client.receive_messages()

    except KeyboardInterrupt:
        print(TerminalColors.colorize("\nStopping client...", TerminalColors.YELLOW))
    except Exception as e:
        print(TerminalColors.colorize(f"Error in main: {e}", TerminalColors.RED))
    finally:
        if client.websocket and client.websocket.open:
            await client.websocket.close()
        print(TerminalColors.colorize("Connection closed", TerminalColors.YELLOW))

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        signal_handler()
