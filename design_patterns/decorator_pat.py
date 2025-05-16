from functools import wraps
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Time logging decorator
def log_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"Function '{func.__name__}' took {execution_time:.4f} seconds to execute")
        return result
    return wrapper

# Parent class (Component)
class TextOutput:
    @log_time
    def get_output(self, text: str) -> str:
        """Returns plain text output with a long loop for delay."""
        # Simulate heavy computation with a long loop
        for _ in range(10_000_000):
            pass
        return text

# Child class (Decorator)
class BoldTextDecorator(TextOutput):
    def __init__(self, wrapped: TextOutput):
        self._wrapped = wrapped
    
    @log_time
    def get_output(self, text: str) -> str:
        """Wraps the parent class method to return bold HTML text."""
        # Simulate heavy computation with a long loop
        for _ in range(5_000_000):  # Slightly shorter loop for decorator
            pass
        return f"<b>{self._wrapped.get_output(text)}</b>"
    
    @log_time
    def get_output_bold(self, text: str) -> str:
        """Dedicated method to return bold HTML text with a long loop."""
        # Simulate heavy computation with a long loop
        for _ in range(5_000_000):
            pass
        return f"<b>{text}</b>"

# Demonstration
def main():
    # Create plain text output
    plain_text = TextOutput()
    result1 = plain_text.get_output("Hello, World!")
    logger.info(f"Plain output: {result1}")
    
    # Create bold text decorator
    bold_text = BoldTextDecorator(plain_text)
    result2 = bold_text.get_output("Hello, World!")
    logger.info(f"Decorated output (get_output): {result2}")
    
    result3 = bold_text.get_output_bold("Hello, World!")
    logger.info(f"Decorated output (get_output_bold): {result3}")

if __name__ == "__main__":
    main()