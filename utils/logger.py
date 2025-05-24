import logging
import os

# Create logs directory if it doesn't exist
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)

# Setup logging
log_file = os.path.join(log_dir, 'honeypot.log')
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def log_event(message):
    logging.info(message)
    print(message)  # Optional: Print to console for debugging
