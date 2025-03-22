import requests
import json
from config import PORT, HOST


def test_vendor_qualification():
    url = f"http://{HOST}:{PORT}/vendor_qualification"
    # payload = {
    #     "software_category": "Accounting & Finance Software",
    #     "capabilities": ["Budgeting", "Accounting", "Planning", ""],
    #     "similarity_method": "tfidf",
    #     "threshold": 0.2,  
    # }
    # payload = {
    #     "software_category": "Accounting & Finance Software",
    #     "capabilities": ["Budgeting", "Accounting", "Planning", ""],
    #     "similarity_method": "cosine",
    #     "threshold": 0.5,  
    # }
    # payload = {
    #     "software_category": "Accounting & Finance Software",
    #     "capabilities": ["Budgeting", "Accounting", "Planning", ""],
    #     "similarity_method": "sbert",
    #     "threshold": 0.1,  
    # }
    payload = {
        "software_category": "Accounting & Finance Software",
        "capabilities": ["Budgeting", "Accounting", "Planning", ""],
        "similarity_method": "openai",
        "threshold": 0.2,  
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for 4XX/5XX responses

        print("Status Code:", response.status_code)
        print("Response:")
        print(json.dumps(response.json(), indent=2))

        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None


if __name__ == "__main__":
    print("Testing Vendor Qualification API...")
    print(f"Sending request to: http://{HOST}:{PORT}/vendor_qualification")
    test_vendor_qualification()
