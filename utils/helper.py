import re
import logging
import time
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def format_time(seconds):
    """
    Format seconds into a readable time string

    Args:
        seconds (float): Time in seconds

    Returns:
        str: Formatted time string
    """
    if seconds < 1:
        return f"{seconds * 1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    else:
        minutes = int(seconds // 60)
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds:.0f}s"


def log_execution_time(func):
    """
    Decorator to log function execution time

    Args:
        func: Function to decorate

    Returns:
        wrapper: Decorated function
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.info(f"{func.__name__} executed in {format_time(elapsed_time)}")
        return result

    return wrapper


def sanitize_query(query):
    """
    Sanitize user query by removing special characters

    Args:
        query (str): User query

    Returns:
        str: Sanitized query
    """
    # Remove any potentially harmful characters
    sanitized = re.sub(r'[^\w\s.,;:?!()\[\]{}"\'`-]', '', query)
    return sanitized.strip()


def extract_cdp_name(query):
    """
    Try to extract CDP name from query

    Args:
        query (str): User query

    Returns:
        str or None: Extracted CDP name or None
    """
    query = query.lower()
    cdps = {
        "segment": ["segment", "segments"],
        "mparticle": ["mparticle", "m particle", "m-particle"],
        "lytics": ["lytics", "lytic"],
        "zeotap": ["zeotap", "zeo tap", "zeo-tap"]
    }

    for cdp, aliases in cdps.items():
        for alias in aliases:
            if alias in query:
                return cdp

    return None


def determine_query_type(query):
    """
    Try to determine query type from query text

    Args:
        query (str): User query

    Returns:
        str: Query type
    """
    query = query.lower()

    # Check for comparison keywords
    comparison_keywords = ["compare", "comparison", "difference", "differences",
                           "versus", "vs", "better", "best"]
    for keyword in comparison_keywords:
        if keyword in query:
            return "Cross-CDP Comparison"

    # Check for advanced configuration keywords
    advanced_keywords = ["advanced", "configuration", "complex", "custom", "integrate",
                         "integration", "setup", "implement", "implementation"]
    for keyword in advanced_keywords:
        if keyword in query:
            return "Advanced Configuration"

    # Default to how-to
    return "How-to Question"


def generate_example_questions(cdp=None):
    """
    Generate example questions based on CDP

    Args:
        cdp (str, optional): CDP name

    Returns:
        dict: Dictionary of example questions by query type
    """
    examples = {
        "How-to Question": [
            "How do I set up a new source?",
            "How can I create a user profile?",
            "How do I build an audience segment?",
            "How can I integrate my data?"
        ],
        "Cross-CDP Comparison": [
            "How does audience creation process compare?",
            "What are the differences in data collection?",
            "Compare user identification methods",
            "Which CDP has better data export capabilities?"
        ],
        "Advanced Configuration": [
            "How to implement server-side tracking?",
            "Advanced custom attribute mapping?",
            "Setting up real-time personalization?",
            "Configure multi-channel identity resolution?"
        ]
    }

    # If CDP is specified, make examples more specific
    if cdp:
        for query_type in examples:
            examples[query_type] = [q.replace("?", f" in {cdp}?") for q in examples[query_type]]

    return examples