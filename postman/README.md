# Postman Testing Collection

This folder contains a Postman collection for testing the TradingView to MT5 Integration API endpoints.

## Getting Started

### 1. Import the Collection

- Open Postman
- Click "Import" > "File" > select `tradingview-alerts-to-metatrader5.postman_collection.json`

### 2. Configure the Environment

- Create a new environment in Postman
- Add a variable `baseUrl` with the value of your Ngrok URL (e.g., `https://xxxx.ngrok-free.app`)
- Select this environment in the environment dropdown

### 3. Run Requests

The collection includes the following requests for testing different parts of the API:

## Available Endpoints

| Endpoint               | Method | Description                               | Request Body                                               | Response                                                      |
| ---------------------- | ------ | ----------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------- |
| `/`                    | GET    | Root endpoint with API information        | None                                                       | JSON object with API details and available endpoints          |
| `/health`              | GET    | Health check endpoint                     | None                                                       | `{"status": "ok", "mt5_connected": true, "timestamp": "..."}` |
| `/trade`               | POST   | Main endpoint for TradingView alerts      | `{"symbol": "EURUSD", "side": "BUY", "volume": 0.01, ...}` | Success or error response with trade details                  |
| `/positions`           | GET    | List all open positions                   | None                                                       | Array of position objects with details                        |
| `/position/<id>/close` | POST   | Close a specific position                 | None                                                       | Success or error response                                     |
| `/symbols`             | GET    | List all available symbols                | None                                                       | Array of available symbols                                    |
| `/symbols?q=EUR`       | GET    | Search for symbols containing "EUR"       | None                                                       | Filtered array of symbols                                     |
| `/trade`               | POST   | Alternative endpoint for executing trades | `{"symbol": "EURUSD", "side": "BUY", "volume": 0.01}`      | Success or error response with trade details                  |

## Key Tests to Run

### Testing Connectivity

1. Run the `health` request to verify the server is running and MT5 is connected
2. Run the `root` request to see all available endpoints

### Testing Symbol Handling

1. Run the `allSymbols` request to see all available symbols in MT5
2. Use the `symbol` request with different query parameters to search for specific symbols

### Testing Trade Execution

1. Modify the `trade` request body with:
   ```json
   {
     "symbol": "EURUSD",
     "side": "BUY",
     "volume": 0.01
   }
   ```
2. Send the request to execute a trade
3. Check the response for success and verify in MT5 that the trade was placed

### Testing Position Management

1. Run the `positions` request to view all open positions
2. To close a position, note its ID and use it in the `/position/<id>/close` endpoint

## Troubleshooting

- Make sure you include the `ngrok-skip-browser-warning: true` header for all requests
- Verify your Ngrok URL is correctly set in the Postman environment
- If you get connection errors, check that both the Flask server and Ngrok are running
- If you get symbol errors, verify the exact format your broker uses with the `/symbols` endpoint
