import requests
from bs4 import BeautifulSoup
import re
import csv
import time

BASE_CA = "/etc/ssl/certs/ca-certificates.crt"
HEADERS = {"User-Agent": "Mozilla/5.0"}

DELAY = 2


def search_duckduckgo(query):
    url = "https://html.duckduckgo.com/html/"
    try:
        response = requests.post(
            url,
            data={"q": query},
            headers=HEADERS,
            verify=BASE_CA,
            timeout=10
        )
        return response.text
    except:
        return ""


def extract_phone_from_html(html):
    phones = re.findall(r'(\+8801[3-9]\d{8}|8801[3-9]\d{8}|01[3-9]\d{8})', html)
    return phones[0] if phones else ""


def extract_page_name(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=8, verify=BASE_CA)
        soup = BeautifulSoup(response.text, "lxml")
        if soup.title:
            return soup.title.text.strip().replace("| Facebook", "")
    except:
        pass
    return ""


def main():
    enriched = []

    with open("data/facebook_leads.csv", newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            fb_url = row["FacebookPage"]
            print(f"\n🔎 Processing: {fb_url}")

            page_name = extract_page_name(fb_url)

            if not page_name:
                continue

            query = f'"{page_name}" Bangladesh phone'
            html = search_duckduckgo(query)

            phone = extract_phone_from_html(html)

            print(f"✅ Found phone: {phone}")

            enriched.append([fb_url, page_name, phone])

            time.sleep(DELAY)

    with open("data/facebook_enriched.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["FacebookPage", "BusinessName", "Phone"])
        writer.writerows(enriched)

    print("\n✅ Facebook leads enriched with phone numbers.")


if __name__ == "__main__":
    main()
