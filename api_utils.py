import json
import os
import pandas as pd
from datetime import datetime

DATA_DIR = "./"  # where your JSON files live
CSV_FILE = "messages.csv"  # your message log

def fetch_company_data(company_name: str) -> dict:
    """
    Looks for a JSON file matching the company name.
    Returns full JSON data as dict.
    """
    filename = f"{company_name.lower().replace(' ', '_')}.json"
    path = os.path.join(DATA_DIR, filename)
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"No data found for company '{company_name}' at {path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data


def save_message_to_csv(company: str, person: str, role: str, message: str):
    """
    Saves a generated LinkedIn message to CSV with metadata.
    """
    word_count = len(message.split())
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entry = {
        "Company": company,
        "Person": person,
        "Role": role,
        "Message": message,
        "Word Count": word_count,
        "Timestamp": timestamp
    }

    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    else:
        df = pd.DataFrame([entry])

    df.to_csv(CSV_FILE, index=False)
    return {"status": "success", "message": "Saved to CSV"}
