"""
Payment Gateway Modules
"""

from .base import BaseGateway
from .stripe import StripeGateway
from .braintree import BraintreeGateway

# Gateway registry
GATEWAY_MODULES = {
    'stripe': StripeGateway,
    'braintree': BraintreeGateway,
}

def get_gateway_handler(gateway_name, keys, config=None):
    """
    Get appropriate gateway handler
    
    Args:
        gateway_name (str): Name of the gateway
        keys (list): API keys
        config (dict): Additional configuration
        
    Returns:
        BaseGateway: Gateway handler instance
    """
    gateway_class = GATEWAY_MODULES.get(gateway_name.lower())
    
    if gateway_class:
        return gateway_class(keys, config)
    
    return None

__all__ = ['BaseGateway', 'StripeGateway', 'BraintreeGateway', 'get_gateway_handler', 'GATEWAY_MODULES']
