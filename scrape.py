import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os

URL = "https://petition.parliament.uk/petitions/722903"
CSV_FILE = "signatures.csv"

def get_signature_count():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(URL, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        count_element = soup.find("span", class_="signature-count-number")
        if count_element:
            print(f"✅ Found count element: {count_element.text}")
            return int(count_element.text.replace(",", ""))
        else:
            print("❌ Could not find the signature-count-number element.")
    except Exception as e:
        print(f"Error: {e}")
    return None

def log_signature_count():
    count = get_signature_count()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if count is not None:
        exists = os.path.isfile(CSV_FILE)
        with open(CSV_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            if not exists:
                writer.writerow(["Timestamp", "Signatures"])
            writer.writerow([timestamp, count])
        print(f"[{timestamp}] ✅ Signatures: {count}")
    else:
        print(f"[{timestamp}] ❌ Failed to get count.")

log_signature_count()
