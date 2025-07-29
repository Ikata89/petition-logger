import asyncio
from playwright.async_api import async_playwright
import csv
from datetime import datetime
import os

CSV_FILE = "signatures.csv"
URL = "https://petition.parliament.uk/petitions/722903"

async def get_signature_count():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(URL, timeout=60000)
        try:
            # Wait for the span to load
            await page.wait_for_selector('span.signature-count-number', timeout=10000)
            count_text = await page.inner_text('span.signature-count-number')
            await browser.close()
            return int(count_text.replace(",", ""))
        except Exception as e:
            print("❌ Could not find signature count:", e)
            await browser.close()
            return None

async def log_signature_count():
    count = await get_signature_count()
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

asyncio.run(log_signature_count())
