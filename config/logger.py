from loguru import logger
import sys

# Configure logging
logger.remove()  # Remove default handlers
logger.add(sys.stdout, format="{time} {level} {message}", level="DEBUG")
logger.add("logs/app.log", rotation="10MB", retention="7 days", level="INFO")

# Example usage
logger.info("Logging Initialized!")
