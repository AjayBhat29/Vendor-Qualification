import pandas as pd
import re


def load_data(file_path):
    """
    Load vendor data from CSV file.

    Args:
        file_path: Path to the CSV file

    Returns:
        DataFrame containing vendor data
    """
    df = pd.read_csv(file_path)

    # Clean up data - handle missing values
    df["Features"] = df["Features"].fillna("")
    df["main_category"] = df["main_category"].fillna("")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

    return df


def preprocess_data(df):
    """
    Preprocess vendor data for similarity calculation.

    Args:
        df: DataFrame containing vendor data

    Returns:
        DataFrame with preprocessed data
    """
    # Function to extract feature information from JSON
    def extract_features(json_str):
        if not json_str or json_str == "":
            return ""

        try:
            # Parse JSON string
            features_data = json.loads(json_str)

            # Extract feature names and descriptions
            all_features = []
            for category in features_data:
                if "features" in category:
                    for feature in category["features"]:
                        feature_name = feature.get("name", "")
                        feature_desc = feature.get("description", "")
                        if feature_name:
                            all_features.append(feature_name)
                        if feature_desc:
                            all_features.append(feature_desc)

            # Join all feature information
            return " ".join(all_features).lower()
        except:
            # Fallback to original string if JSON parsing fails
            return str(json_str).lower()

    # Apply extraction to Features column
    df["Features_processed"] = df["Features"].apply(extract_features)

    # Clean up processed features
    df["Features_processed"] = df["Features_processed"].apply(
        lambda x: re.sub(r"[^\w\s]", " ", str(x)).strip() if pd.notnull(x) else ""
    )

    return df


def filter_by_category(df, category):
    """
    Filter vendors by software category.

    Args:
        df: DataFrame containing vendor data
        category: Software category to filter by

    Returns:
        DataFrame filtered by category
    """
    return df[df["main_category"] == category].copy()
