# Data settings
DATA_FILE_PATH = 'data/G2 software product overview.csv'

# Similarity method settings
DEFAULT_SIMILARITY_METHOD = 'tfidf'

# Default thresholds for different similarity methods
SIMILARITY_THRESHOLDS = {
    'tfidf': 0.3,
    'sbert': 0.75,
    'openai': 0.8
}

# Ranking weights
SIMILARITY_WEIGHT = 0.7
RATING_WEIGHT = 0.3

# API settings
DEBUG_MODE = True
HOST = '0.0.0.0'
PORT = 5001
