from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from config import SIMILARITY_THRESHOLDS

def compute_similarity_tfidf(query_features, vendor_features):
    """
    Compute similarity using TF-IDF and cosine similarity.
    
    Args:
        query_features: String of query features
        vendor_features: List of vendor feature strings
        
    Returns:
        Numpy array of similarity scores
    """
    # Initialize TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(stop_words='english')
    
    # Combine query and vendor features for vectorization
    all_features = [query_features] + vendor_features
    
    # Fit and transform to get TF-IDF matrix
    tfidf_matrix = vectorizer.fit_transform(all_features)
    
    # Calculate cosine similarity between query and each vendor
    similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
    
    return similarities[0]

def compute_similarity_sbert(query_features, vendor_features):
    """
    Compute similarity using Sentence-BERT embeddings.
    
    Args:
        query_features: String of query features
        vendor_features: List of vendor feature strings
        
    Returns:
        Numpy array of similarity scores
    """
    # Placeholder implementation - in a real scenario, you would use SBERT
    print("Note: Using TF-IDF as fallback for SBERT")
    return compute_similarity_tfidf(query_features, vendor_features)

def compute_similarity_openai(query_features, vendor_features):
    """
    Compute similarity using OpenAI embeddings.
    
    Args:
        query_features: String of query features
        vendor_features: List of vendor feature strings
        
    Returns:
        Numpy array of similarity scores
    """
    # Placeholder implementation - in a real scenario, you would use OpenAI API
    print("Note: Using TF-IDF as fallback for OpenAI embeddings")
    return compute_similarity_tfidf(query_features, vendor_features)

def compute_similarity(query_features, vendor_features, method='tfidf'):
    """
    Compute similarity using the specified method.
    
    Args:
        query_features: String of query features
        vendor_features: List of vendor feature strings
        method: Similarity method to use ('tfidf', 'sbert', 'openai')
        
    Returns:
        Numpy array of similarity scores
    """
    if method == 'sbert':
        return compute_similarity_sbert(query_features, vendor_features)
    elif method == 'openai':
        return compute_similarity_openai(query_features, vendor_features)
    else:
        return compute_similarity_tfidf(query_features, vendor_features)

def filter_vendors_by_similarity(df, capabilities, method='tfidf', threshold=None):
    """
    Filter vendors by feature similarity.
    
    Args:
        df: DataFrame containing vendor data (already filtered by category)
        capabilities: List of required capabilities/features
        method: Method to use for similarity calculation
        threshold: Similarity threshold (if None, uses default for the method)
        
    Returns:
        DataFrame of vendors with similarity scores
    """
    if df.empty:
        return df
    
    # Use default threshold if not specified
    if threshold is None:
        threshold = SIMILARITY_THRESHOLDS.get(method, 0.3)
    
    # Convert capabilities list to a single string for comparison
    query_features = ' '.join(capabilities).lower()
    
    # Get all vendor features
    vendor_features = df['Features_processed'].tolist()
    
    # Compute similarity scores
    similarity_scores = compute_similarity(query_features, vendor_features, method)
    
    # Add similarity scores to dataframe
    df['similarity_score'] = similarity_scores
    
    # Filter vendors with similarity score above threshold
    qualified_vendors = df[df['similarity_score'] >= threshold]
    
    return qualified_vendors
