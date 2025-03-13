import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MT5 Configuration
MT5_ACCOUNT = int(os.getenv('MT5_ACCOUNT', 12345678))
MT5_PASSWORD = os.getenv('MT5_PASSWORD', 'your-password')
MT5_SERVER = os.getenv('MT5_SERVER', 'your-broker-server')
MT5_PATH = os.getenv('MT5_PATH', r"C:\Program Files\MetaTrader 5\terminal64.exe")

# MT5 Symbol Settings
MT5_DEFAULT_SUFFIX = os.getenv('MT5_DEFAULT_SUFFIX', '')  # For brokers that use suffixes like '.r'

# Trading Parameters
DEFAULT_VOLUME = float(os.getenv('DEFAULT_VOLUME', 0.01))
DEFAULT_STOP_LOSS = float(os.getenv('DEFAULT_STOP_LOSS', 100))
DEFAULT_TAKE_PROFIT = float(os.getenv('DEFAULT_TAKE_PROFIT', 200))

# Server Configuration
FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 't')

# Ngrok Configuration
NGROK_AUTH_TOKEN = os.getenv('NGROK_AUTH_TOKEN', 'your-ngrok-auth-token')

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Create log directory if it doesn't exist
os.makedirs(LOG_DIR, exist_ok=True)