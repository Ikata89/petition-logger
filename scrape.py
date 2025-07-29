import requests
import os
import json
from datetime import datetime

URL = "https://petition.parliament.uk/petitions/722903.json"
DATA_DIR = "data"

def fetch_petition_json():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("❌ Error fetching JSON:", e)
        return None

def save_snapshot(data):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    filename = os.path.join(DATA_DIR, f"{timestamp}.json")
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Saved snapshot to {filename}")

def main():
    data = fetch_petition_json()
    if data:
        save_snapshot(data)

main()
