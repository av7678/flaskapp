
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit

# Initialize Flask app
app = Flask(__name__)
# Configure CORS with specific origins for security (replace '*' with your frontend URL in production)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for development

# Initialize SocketIO with Flask app
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow all origins for development

# Route to verify server is running
@app.route('/')
def index():
    return "WebSocket server is running!"

# WebSocket event handler for 'sync_event'
@socketio.on('sync_event')
def handle_sync_event(data):
    try:
        print(f"Received sync event: {data}")
        # Broadcast the received data to all connected clients
        emit('sync_broadcast', data, broadcast=True)
    except Exception as e:
        print(f"Error handling sync event: {e}")
        emit('error', {'error': 'Failed to process sync event'}, broadcast=False)

# Run the app with SocketIO
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)  # Enable debug for development
