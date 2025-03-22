from flask import Flask
from src.data_preprocessing import load_data, preprocess_data
from src.api import api_bp
from config import DATA_FILE_PATH, DEBUG_MODE, HOST, PORT

def create_app():
    """
    Create and configure the Flask application.
    
    Returns:
        Configured Flask application
    """
    app = Flask(__name__)
    
    # Load and preprocess data
    df = load_data(DATA_FILE_PATH)
    df = preprocess_data(df)
    
    # Store the dataframe in the app config
    app.config['VENDOR_DATA'] = df
    
    # Register blueprints
    app.register_blueprint(api_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=DEBUG_MODE, host=HOST, port=PORT)