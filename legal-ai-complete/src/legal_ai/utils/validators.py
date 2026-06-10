"""Input validation utilities."""

import logging

logger = logging.getLogger(__name__)


def validate_user_input(user_input: str, max_length: int = 5000) -> bool:
    """
    Validate user input for contract generation.
    
    Args:
        user_input: User's contract description
        max_length: Maximum allowed input length
    
    Returns:
        True if valid, False otherwise
    """
    if not user_input or not user_input.strip():
        logger.warning("Empty user input provided")
        return False
    
    if len(user_input) > max_length:
        logger.warning(f"User input exceeds max length of {max_length} characters")
        return False
    
    return True


def validate_api_key(api_key: str) -> bool:
    """
    Validate API key format.
    
    Args:
        api_key: Gemini API key
    
    Returns:
        True if valid format, False otherwise
    """
    if not api_key or not isinstance(api_key, str):
        logger.error("Invalid API key format")
        return False
    
    if api_key.startswith("#") or "PASTE" in api_key:
        logger.error("API key appears to be placeholder")
        return False
    
    return True
