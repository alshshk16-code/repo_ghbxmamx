"""
Base Gateway Module
Abstract base class for all payment gateway handlers
"""

from abc import ABC, abstractmethod

class BaseGateway(ABC):
    """Abstract base class for payment gateway handlers"""
    
    def __init__(self, keys, config=None):
        """
        Initialize gateway handler
        
        Args:
            keys (list): List of API keys
            config (dict): Additional configuration
        """
        self.keys = keys
        self.config = config or {}
        self.gateway_name = self.__class__.__name__.replace('Gateway', '').lower()
    
    @abstractmethod
    def generate_code(self):
        """
        Generate Python code snippet for this gateway
        
        Returns:
            str: Python code as string
        """
        pass
    
    @abstractmethod
    def get_test_cards(self):
        """
        Get test card numbers for this gateway
        
        Returns:
            dict: Test card information
        """
        pass
    
    def get_primary_key(self):
        """
        Get the primary (first) API key
        
        Returns:
            str: Primary API key
        """
        return self.keys[0] if self.keys else None
    
    def format_code(self, code):
        """
        Format code with proper indentation
        
        Args:
            code (str): Code to format
            
        Returns:
            str: Formatted code
        """
        lines = code.split('\n')
        formatted = []
        
        for line in lines:
            # Remove excessive blank lines
            if line.strip() or (formatted and formatted[-1].strip()):
                formatted.append(line)
        
        return '\n'.join(formatted)
