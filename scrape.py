import requests
import csv
from datetime import datetime
import os

URL = "https://petition.parliament.uk/petitions/722903.json"
CSV_FILE = "signatures.csv"

def get_signature_count():
    try:
        response = requests.get(URL)
        data = response.json()
        count = data["data"]["attributes"]["signature_count"]
        return int(count)
    except Exception as e:
        print("❌ Failed to parse JSON:", e)
        return None

def log_signature_count():
    count = get_signature_count()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if count is not None:
        print(f"[{timestamp}] ✅ Signatures: {count}")
        exists = os.path.isfile(CSV_FILE)
        with open(CSV_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            if not exists:
                writer.writerow(["Timestamp", "Signatures"])
            writer.writerow([timestamp, count])
    else:
        print(f"[{timestamp}] ❌ Failed to get count.")

log_signature_count()
