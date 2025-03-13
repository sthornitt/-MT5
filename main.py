import os
import time
import threading
import argparse
import sys
from app.utils import setup_logging
from app.mt5_handler import MT5Handler
from app.server import run_server

# Set up logging
logger = setup_logging('main')

def start_server(mt5_handler=None):
    """Start the Flask server directly in the main process"""
    logger.info("Starting TradingView to MT5 integration application")
    
    # Create MT5 handler if not provided
    if mt5_handler is None:
        mt5_handler = MT5Handler()
    
    # Start the server
    run_server(mt5_handler)

def start_ngrok():
    """Start Ngrok in a separate process"""
    logger.info("Starting Ngrok tunnel")
    
    # Import here to avoid importing if not used
    from subprocess import Popen
    
    # Get the path to the ngrok setup script
    ngrok_script = os.path.join(os.path.dirname(__file__), 'scripts', 'ngrok_setup.py')
    
    # Start Ngrok in a separate process
    Popen([sys.executable, ngrok_script])

def main():
    """Main entry point for the application"""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='TradingView to MT5 integration')
    parser.add_argument('--no-ngrok', action='store_true', help='Do not start Ngrok automatically')
    parser.add_argument('--test-mt5', action='store_true', help='Test MT5 connection and exit')
    parser.add_argument('--ngrok-only', action='store_true', help='Start only Ngrok without Flask server')
    args = parser.parse_args()
    
    # Test MT5 connection if requested
    if args.test_mt5:
        from scripts.test_mt5_connection import test_mt5_connection
        test_mt5_connection()
        return
    
    # Create MT5 handler
    mt5_handler = MT5Handler()
    
    try:
        # Option to start only Ngrok (useful for debugging)
        if args.ngrok_only:
            start_ngrok()
            logger.info("Started Ngrok only. Press Ctrl+C to exit.")
            while True:
                time.sleep(1)
            return
        
        # Start Ngrok in a separate process if not disabled
        if not args.no_ngrok:
            ngrok_process = threading.Thread(target=start_ngrok)
            ngrok_process.daemon = True
            ngrok_process.start()
            time.sleep(2)  # Give Ngrok time to start
        
        # Run the server in the main thread
        logger.info("Starting Flask server...")
        start_server(mt5_handler)
            
    except KeyboardInterrupt:
        logger.info("Application terminated by user")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
    finally:
        logger.info("Shutting down application")
        try:
            if 'mt5_handler' in locals():
                mt5_handler.close_session()
        except Exception as e:
            logger.error(f"Error during shutdown: {str(e)}")

if __name__ == "__main__":
    main()