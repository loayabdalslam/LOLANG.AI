import asyncio
import json
import logging
import signal
import sys
from websockets.server import serve
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

class AgentServer:
    def __init__(self):
        self.config = GeminiConfig.get_default_config()
        self.agent = AIAgent("Server-Agent", TerminalColors.BLUE, self.config)
        self.decryptor = LolangDecryptor(self.config)
        self.visualizer = MessageVisualizer()
        self.clients = set()
        self.response_history = []
        self.running = True

    async def register(self, websocket):
        self.clients.add(websocket)
        print(TerminalColors.colorize(f"Client connected. Total clients: {len(self.clients)}", TerminalColors.YELLOW))

    async def unregister(self, websocket):
        self.clients.remove(websocket)
        print(TerminalColors.colorize(f"Client disconnected. Total clients: {len(self.clients)}", TerminalColors.YELLOW))

    async def process_message(self, websocket, message):
        data = json.loads(message)
        content = data.get("content", "")
        role = data.get("role", "user")

        # Add message to history
        self.response_history.append({"role": role, "content": content})

        # Still decrypt for internal processing but don't display
        decrypted_client_message = await self.decryptor.decrypt(content)

        # Visualize client message without decryption
        print(self.visualizer.visualize_message(role, content))

        # Generate response
        response = self.agent.chat(self.response_history)
        formatted_response = response.strip().replace('\n', ' ').replace('  ', ' ')

        # Still decrypt for internal processing but don't display
        decrypted_server_response = await self.decryptor.decrypt(formatted_response)

        # Visualize server response without decryption
        print(self.visualizer.visualize_server_message(formatted_response))

        # Add to history
        self.response_history.append({"role": "server-agent", "content": formatted_response})

        # Send response to all clients (without decrypted content)
        await self.broadcast(json.dumps({
            "role": "server-agent",
            "content": formatted_response
        }))

    async def broadcast(self, message):
        if self.clients:
            await asyncio.gather(
                *[client.send(message) for client in self.clients]
            )

    async def handler(self, websocket, path):
        await self.register(websocket)
        try:
            async for message in websocket:
                if not self.running:
                    break
                await self.process_message(websocket, message)
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            await self.unregister(websocket)

    def stop(self):
        self.running = False
        print(TerminalColors.colorize("Server stopping...", TerminalColors.YELLOW))

# Handle Ctrl+C for Windows
def signal_handler():
    print(TerminalColors.colorize("\nStopping server...", TerminalColors.YELLOW))
    sys.exit(0)

async def main():
    agent_server = AgentServer()

    # Handle graceful shutdown based on platform
    if sys.platform != 'win32':
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, agent_server.stop)
    else:
        # Windows doesn't support add_signal_handler
        # We'll rely on KeyboardInterrupt exception instead
        pass

    server = await serve(agent_server.handler, "localhost", 8765)
    print("Server started at ws://localhost:8765")
    print("Press Ctrl+C to stop the server")

    try:
        while agent_server.running:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print(TerminalColors.colorize("\nStopping server...", TerminalColors.YELLOW))
    finally:
        server.close()
        await server.wait_closed()
        print(TerminalColors.colorize("Server closed", TerminalColors.YELLOW))

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        signal_handler()


