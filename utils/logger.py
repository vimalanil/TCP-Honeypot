import logging
import os
from datetime import datetime

# Define log directory path
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

# Log file path
LOG_FILE = os.path.join(LOG_DIR, 'honeypot.log')

# Logging configuration
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log_event(message: str):
    """Log the event to file and print to console."""
    logging.info(message)
    print(f"[LOG] {datetime.now().strftime('%H:%M:%S')} - {message}")
