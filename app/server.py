import logging
import threading
from .mt5_handler import MT5Handler
from .utils import parse_tradingview_webhook
from .config import FLASK_HOST, FLASK_PORT, DEBUG
from flask import Flask, request, jsonify

logger = logging.getLogger(__name__)

def create_app(mt5_handler=None):
    """
    Create and configure the Flask application
    
    Args:
        mt5_handler (MT5Handler, optional): MT5 handler instance. Creates new one if None.
        
    Returns:
        Flask: Configured Flask application
    """
    app = Flask(__name__)
    
    # Create MT5 handler if not provided
    if mt5_handler is None:
        mt5_handler = MT5Handler()

    @app.route('/symbols', methods=['GET'])
    def get_symbols():
        """Endpoint to get all available symbols"""
        try:
            symbols = mt5_handler.list_available_symbols()
            
            # Filter by query if provided
            query = request.args.get('q', '').upper()
            if query:
                symbols = [s for s in symbols if query in s.upper()]
            
            return jsonify({
                "success": True,
                "count": len(symbols),
                "symbols": symbols
            }), 200
            
        except Exception as e:
            logger.error(f"Error getting symbols: {str(e)}", exc_info=True)
            return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500

    @app.route('/', methods=['GET'])
    def index():
        """Root endpoint with basic information"""
        return jsonify({
            "name": "TradingView to MT5 Integration",
            "version": "1.0.0",
            "status": "running",
            "mt5_connected": mt5_handler.connected,
            "endpoints": {
                "/": "This information page (GET)",
                "/trade": "Endpoint for TradingView alerts (POST)",
                "/health": "Health check endpoint (GET)",
                "/positions": "List open positions (GET)",
                "/position/<id>/close": "Close a specific position (POST)",
                "/symbols": "List available symbols (GET)",
                "/symbols?q=EUR": "Search for symbols (GET)"
            }
        })

    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint to verify the server is running"""
        return jsonify({
            "status": "ok", 
            "mt5_connected": mt5_handler.connected,
            "timestamp": str(import_datetime().now())
        })

    @app.route('/trade', methods=['POST'])
    def webhook():
        """Endpoint to receive TradingView alerts"""
        if request.method == 'POST':
            try:
                # Log the request
                logger.info(f"Received webhook request from {request.remote_addr}")
                
                # Get the JSON data from TradingView
                if not request.is_json:
                    logger.warning("Request is not JSON")
                    return jsonify({"success": False, "message": "Request must be JSON"}), 400
                
                data = request.json
                logger.info(f"Received webhook data: {data}")
                
                # Parse and validate the webhook data
                try:
                    trade_params = parse_tradingview_webhook(data)
                except ValueError as e:
                    logger.error(f"Invalid webhook data: {str(e)}")
                    return jsonify({"success": False, "message": str(e)}), 400
                
                # Place the trade
                result = mt5_handler.place_trade(
                    symbol=trade_params['symbol'],
                    order_type=trade_params['side'],
                    volume=trade_params['volume'],
                    price=trade_params['price'],
                    stop_loss=trade_params['stop_loss'],
                    take_profit=trade_params['take_profit'],
                    comment=trade_params['comment']
                )
                
                # Return the result
                if result['success']:
                    logger.info(f"Trade executed successfully: {result['message']}")
                    return jsonify(result), 200
                else:
                    logger.error(f"Trade execution failed: {result['message']}")
                    return jsonify(result), 500
            
            except Exception as e:
                logger.error(f"Error processing webhook: {str(e)}", exc_info=True)
                return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500
        
        return jsonify({"success": False, "message": "Invalid request method"}), 405
    
    @app.route('/positions', methods=['GET'])
    def get_positions():
        """Endpoint to get all open positions"""
        try:
            # Get symbol from query string if provided
            symbol = request.args.get('symbol')
            
            # Get positions
            positions = mt5_handler.get_positions(symbol)
            
            return jsonify({
                "success": True,
                "positions": positions,
                "count": len(positions)
            }), 200
            
        except Exception as e:
            logger.error(f"Error getting positions: {str(e)}", exc_info=True)
            return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500
    
    @app.route('/position/<int:position_id>/close', methods=['POST'])
    def close_position(position_id):
        """Endpoint to close a specific position"""
        try:
            # Close the position
            result = mt5_handler.close_position(position_id)
            
            # Return the result
            if result['success']:
                logger.info(f"Position closed successfully: {result['message']}")
                return jsonify(result), 200
            else:
                logger.error(f"Position close failed: {result['message']}")
                return jsonify(result), 500
            
        except Exception as e:
            logger.error(f"Error closing position: {str(e)}", exc_info=True)
            return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500
    
    @app.errorhandler(404)
    def not_found(e):
        """Handle 404 errors"""
        return jsonify({"success": False, "message": "Endpoint not found"}), 404
    
    @app.errorhandler(405)
    def method_not_allowed(e):
        """Handle 405 errors"""
        return jsonify({"success": False, "message": "Method not allowed"}), 405
    
    @app.errorhandler(500)
    def server_error(e):
        """Handle 500 errors"""
        return jsonify({"success": False, "message": "Internal server error"}), 500
    
    return app

def import_datetime():
    """Import datetime to avoid circular imports"""
    from datetime import datetime
    return datetime

def run_server(mt5_handler=None):
    """
    Run the Flask server
    
    Args:
        mt5_handler (MT5Handler, optional): MT5 handler instance
    """
    app = create_app(mt5_handler)
    # When running in a thread, we need to disable the reloader
    use_reloader = DEBUG and threading.current_thread() is threading.main_thread()
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=DEBUG, use_reloader=use_reloader)