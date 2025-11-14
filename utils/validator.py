"""
Input validation utilities for Gateway-Ripper
"""

import re
import validators
from urllib.parse import urlparse

class Validator:
    """Validates user inputs and extracted data"""
    
    @staticmethod
    def is_valid_url(url):
        """
        Validate if string is a valid URL
        
        Args:
            url (str): URL to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not url:
            return False
        
        # Add scheme if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Allow localhost for testing
        if 'localhost' in url or '127.0.0.1' in url:
            return True
        
        return validators.url(url) is True
    
    @staticmethod
    def normalize_url(url):
        """
        Normalize URL by adding scheme if missing
        
        Args:
            url (str): URL to normalize
            
        Returns:
            str: Normalized URL
        """
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url
    
    @staticmethod
    def is_stripe_key(key):
        """
        Check if string is a valid Stripe key
        
        Args:
            key (str): Key to validate
            
        Returns:
            bool: True if valid Stripe key
        """
        if not key:
            return False
        
        # Stripe publishable keys start with pk_
        # Stripe secret keys start with sk_
        stripe_pattern = r'^(pk|sk)_(test|live)_[a-zA-Z0-9]{24,}$'
        return bool(re.match(stripe_pattern, key))
    
    @staticmethod
    def is_braintree_token(token):
        """
        Check if string is a valid Braintree token
        
        Args:
            token (str): Token to validate
            
        Returns:
            bool: True if valid Braintree token
        """
        if not token:
            return False
        
        # Braintree tokens are typically base64-like strings
        return len(token) > 20 and token.replace('_', '').replace('-', '').isalnum()
    
    @staticmethod
    def extract_domain(url):
        """
        Extract domain from URL
        
        Args:
            url (str): URL to extract domain from
            
        Returns:
            str: Domain name
        """
        parsed = urlparse(url)
        return parsed.netloc or parsed.path
    
    @staticmethod
    def is_payment_related_url(url):
        """
        Check if URL is related to payment processing
        
        Args:
            url (str): URL to check
            
        Returns:
            bool: True if payment-related
        """
        payment_keywords = [
            'stripe', 'braintree', 'paypal', 'checkout', 'payment',
            'pay', 'billing', 'cart', 'order', 'purchase'
        ]
        
        url_lower = url.lower()
        return any(keyword in url_lower for keyword in payment_keywords)
    
    @staticmethod
    def extract_api_keys(text):
        """
        Extract potential API keys from text
        
        Args:
            text (str): Text to search
            
        Returns:
            list: List of potential API keys
        """
        keys = []
        
        # Stripe keys
        stripe_pattern = r'(pk|sk)_(test|live)_[a-zA-Z0-9]{24,}'
        keys.extend(re.findall(stripe_pattern, text))
        
        # Generic API key patterns
        generic_pattern = r'["\']([a-zA-Z0-9_-]{32,})["\']'
        potential_keys = re.findall(generic_pattern, text)
        
        # Filter out common false positives
        for key in potential_keys:
            if len(key) >= 32 and not key.isdigit():
                keys.append(key)
        
        return list(set(keys))  # Remove duplicates
