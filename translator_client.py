import asyncio
import json
import logging
import signal
import sys
from websockets.client import connect
from terminal_colors import TerminalColors
from config import GeminiConfig
from lolang_decryptor import LolangDecryptor
from message_visualizer import MessageVisualizer

# Set root logger to WARNING to suppress all INFO logs
logging.basicConfig(level=logging.WARNING)
# Only show ERROR logs for our module
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

class TranslatorClient:
    def __init__(self):
        self.config = GeminiConfig.get_default_config()
        self.decryptor = LolangDecryptor(self.config)
        self.visualizer = MessageVisualizer()
        self.websocket = None
        self.running = True
        self.message_count = 0

    async def connect(self, uri):
        self.websocket = await connect(uri)
        return self.websocket

    async def receive_messages(self):
        if not self.websocket:
            logger.error("Not connected to server")
            return

        print(self.visualizer.visualize_system_message("Translator client connected. Translating all LOLANG messages in real-time."))
        print(self.visualizer.visualize_system_message("Press Ctrl+C to stop the translator."))
        print(self.visualizer.visualize_system_message("Waiting for messages..."))
        print("-" * 80)  # Separator for better readability

        try:
            async for message in self.websocket:
                if not self.running:
                    break

                data = json.loads(message)
                content = data.get("content", "")
                role = data.get("role", "server-agent")

                # Determine the color based on the role
                if "server" in role.lower():
                    encrypted_color = TerminalColors.BLUE
                    translated_color = TerminalColors.CYAN
                else:
                    encrypted_color = TerminalColors.GREEN
                    translated_color = TerminalColors.YELLOW

                # Format the role name for display
                display_role = role.replace("-agent", "").title()

                # Decrypt the message
                decrypted_content = await self.decryptor.decrypt(content)

                # Visualize both the encrypted and decrypted messages
                print(TerminalColors.colorize(f"[ENCRYPTED] {display_role}: {content}", encrypted_color))
                print(TerminalColors.colorize(f"[TRANSLATED] {display_role}: {decrypted_content}", translated_color))
                print("-" * 80)  # Separator for better readability

                # Increment message count
                self.message_count += 1

        except Exception as e:
            logger.error(f"Error in receive_messages: {e}")
        finally:
            if self.websocket and self.websocket.open:
                await self.websocket.close()

    def stop(self):
        self.running = False
        print(TerminalColors.colorize("Translator client stopping...", TerminalColors.YELLOW))

# Handle Ctrl+C for Windows
def signal_handler():
    print(TerminalColors.colorize("\nStopping translator client...", TerminalColors.YELLOW))
    sys.exit(0)

async def main():
    translator = TranslatorClient()
    uri = "ws://localhost:8765"

    # Handle graceful shutdown based on platform
    if sys.platform != 'win32':
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, translator.stop)
    else:
        # Windows doesn't support add_signal_handler
        # We'll rely on KeyboardInterrupt exception instead
        pass

    try:
        await translator.connect(uri)
        print(TerminalColors.colorize("Translator connected to server", TerminalColors.HEADER))

        # Start receiving and translating messages
        await translator.receive_messages()

    except KeyboardInterrupt:
        print(TerminalColors.colorize("\nStopping translator client...", TerminalColors.YELLOW))
    except Exception as e:
        print(TerminalColors.colorize(f"Error: {e}", TerminalColors.RED))
    finally:
        if translator.websocket and translator.websocket.open:
            await translator.websocket.close()
        print(TerminalColors.colorize("Connection closed", TerminalColors.YELLOW))

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        signal_handler()
