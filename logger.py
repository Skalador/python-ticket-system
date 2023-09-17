import logging

# Configure the logger
logging.basicConfig(
    level=logging.INFO,  # Set the log level (e.g., INFO, DEBUG, WARNING)
    # Define log message format
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'  # Define date and time format
)
# Create a logger instance
logger = logging.getLogger(__name__)
