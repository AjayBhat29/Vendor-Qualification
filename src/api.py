from flask import Blueprint, request, jsonify, current_app
from src.data_preprocessing import filter_by_category
from src.similarity import filter_vendors_by_similarity
from src.ranking import rank_vendors
import json

api_bp = Blueprint("api", __name__)


@api_bp.route("/vendor_qualification", methods=["POST"])
def vendor_qualification():
    data = request.get_json()

    software_category = data.get("software_category", "")
    capabilities = data.get("capabilities", [])
    similarity_method = data.get("similarity_method", "tfidf")
    threshold = data.get("threshold", None)

    if not software_category or not capabilities:
        return jsonify({"error": "Missing required parameters"}), 400

    df = current_app.config["VENDOR_DATA"]
    category_filtered_df = filter_by_category(df, software_category)

    if category_filtered_df.empty:
        return jsonify(
            {
                "vendors": [],
                "message": f"No vendors found in category: {software_category}",
                "method": similarity_method,
                "threshold": threshold,
            }
        )

    qualified_vendors = filter_vendors_by_similarity(
        category_filtered_df, capabilities, similarity_method, threshold
    )

    if qualified_vendors.empty:
        return jsonify(
            {
                "vendors": [],
                "message": "No vendors match the specified capabilities",
                "method": similarity_method,
                "threshold": threshold,
            }
        )

    ranked_vendors = rank_vendors(qualified_vendors)
    top_vendors = ranked_vendors.head(10)

    result_columns = [
        "product_name",
        "main_category",
        # "Features_processed",
        "similarity_score",
        "final_score",
        "rating",
        "seller",
        "headquarters",
        "year_founded",
    ]

    available_columns = [col for col in result_columns if col in top_vendors.columns]

    result = []
    for _, vendor in top_vendors[available_columns].iterrows():
        vendor_dict = vendor.to_dict()
        try:
            features_json = json.loads(vendor_dict.get("Features", "{}"))
            vendor_dict["Features"] = features_json
        except json.JSONDecodeError:
            vendor_dict["Features"] = {}
        result.append(vendor_dict)

    return jsonify(
        {
            "vendors": result,
            "method": similarity_method,
            "threshold": threshold,
            "total_matches": len(qualified_vendors),
        }
    )
