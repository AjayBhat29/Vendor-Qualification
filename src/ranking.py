from config import SIMILARITY_WEIGHT, RATING_WEIGHT

def rank_vendors(qualified_vendors):
    """
    Rank vendors based on similarity score and rating.
    
    Args:
        qualified_vendors: DataFrame of qualified vendors with similarity scores
        
    Returns:
        DataFrame of ranked vendors
    """
    # Make a copy to avoid modifying the original dataframe
    ranked_vendors = qualified_vendors.copy()
    
    # If rating column exists, use it for ranking
    if 'rating' in ranked_vendors.columns:
        # Normalize rating to be between 0 and 1
        max_rating = ranked_vendors['rating'].max()
        ranked_vendors['normalized_rating'] = ranked_vendors['rating'] / max_rating if max_rating > 0 else 0
        
        # Combine similarity score and rating with configured weights
        ranked_vendors['final_score'] = (
            SIMILARITY_WEIGHT * ranked_vendors['similarity_score'] + 
            RATING_WEIGHT * ranked_vendors['normalized_rating']
        )
    else:
        # Use only similarity score if rating is not available
        ranked_vendors['final_score'] = ranked_vendors['similarity_score']
    
    # Sort by final score in descending order
    ranked_vendors = ranked_vendors.sort_values(by='final_score', ascending=False)
    
    return ranked_vendors