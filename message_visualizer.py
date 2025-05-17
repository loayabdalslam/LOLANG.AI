import logging
from terminal_colors import TerminalColors

class MessageVisualizer:
    """
    A module for visualizing LOLANG messages and their decrypted versions.
    Provides formatted output for better readability.
    """
    
    def __init__(self):
        """
        Initialize the message visualizer.
        """
        self.logger = logging.getLogger(__name__)
    
    def visualize_message(self, role, encrypted_message, decrypted_message=None):
        """
        Visualize a message with its encrypted and optionally decrypted forms.
        
        Args:
            role (str): The role of the message sender (e.g., "Server-Agent", "Client-Agent").
            encrypted_message (str): The original LOLANG encrypted message.
            decrypted_message (str, optional): The decrypted human-readable message.
                If None, only the encrypted message will be displayed.
                
        Returns:
            str: The formatted message for display.
        """
        # Determine color based on role
        if "Server" in role:
            color = TerminalColors.BLUE
        elif "Client" in role:
            color = TerminalColors.GREEN
        else:
            color = TerminalColors.YELLOW
        
        # Format the encrypted message
        formatted_encrypted = TerminalColors.colorize(
            f"{role}: {encrypted_message}", 
            color
        )
        
        # If decrypted message is provided, format it as well
        if decrypted_message:
            formatted_decrypted = TerminalColors.colorize(
                f"[Decrypted] {role}: {decrypted_message}",
                TerminalColors.YELLOW
            )
            return f"{formatted_encrypted}\n{formatted_decrypted}"
        
        return formatted_encrypted
    
    def visualize_client_message(self, encrypted_message, decrypted_message=None):
        """
        Visualize a client message with its encrypted and optionally decrypted forms.
        
        Args:
            encrypted_message (str): The original LOLANG encrypted message.
            decrypted_message (str, optional): The decrypted human-readable message.
                
        Returns:
            str: The formatted client message for display.
        """
        return self.visualize_message("Client-Agent", encrypted_message, decrypted_message)
    
    def visualize_server_message(self, encrypted_message, decrypted_message=None):
        """
        Visualize a server message with its encrypted and optionally decrypted forms.
        
        Args:
            encrypted_message (str): The original LOLANG encrypted message.
            decrypted_message (str, optional): The decrypted human-readable message.
                
        Returns:
            str: The formatted server message for display.
        """
        return self.visualize_message("Server-Agent", encrypted_message, decrypted_message)
    
    def visualize_system_message(self, message):
        """
        Visualize a system message.
        
        Args:
            message (str): The system message to display.
                
        Returns:
            str: The formatted system message for display.
        """
        return TerminalColors.colorize(f"System: {message}", TerminalColors.HEADER)
    
    def visualize_error_message(self, message):
        """
        Visualize an error message.
        
        Args:
            message (str): The error message to display.
                
        Returns:
            str: The formatted error message for display.
        """
        return TerminalColors.colorize(f"Error: {message}", TerminalColors.RED)
