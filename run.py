import os
from app import create_app, socketio

# Create app with the specified configuration
config_name = os.environ.get('FLASK_CONFIG', 'default')
app = create_app(config_name)

if __name__ == '__main__':
    # Use socketio.run instead of app.run to enable WebSocket support
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)