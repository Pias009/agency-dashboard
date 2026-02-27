import csv
import requests
import subprocess
from bs4 import BeautifulSoup
import re
import time

BASE_CA = "/etc/ssl/certs/ca-certificates.crt"
HEADERS = {"User-Agent": "Mozilla/5.0"}

MODEL = "qwen2.5-coder:1.5b"


def get_website_text(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=8, verify=BASE_CA)
        soup = BeautifulSoup(response.text, "lxml")

        # Remove scripts/styles
        for script in soup(["script", "style"]):
            script.extract()

        text = soup.get_text(separator=" ", strip=True)
        return text[:4000]  # limit for model
    except:
        return ""


def basic_social_analysis(url):
    social = {
        "facebook": False,
        "instagram": False,
        "youtube": False,
        "tiktok": False
    }

    try:
        response = requests.get(url, headers=HEADERS, timeout=8, verify=BASE_CA)
        html = response.text.lower()

        if "facebook.com" in html:
            social["facebook"] = True
        if "instagram.com" in html:
            social["instagram"] = True
        if "youtube.com" in html:
            social["youtube"] = True
        if "tiktok.com" in html:
            social["tiktok"] = True

    except:
        pass

    return social


def run_ollama(prompt):
    result = subprocess.run(
        ["ollama", "run", MODEL],
        input=prompt.encode(),
        stdout=subprocess.PIPE
    )
    return result.stdout.decode()


def analyze_lead(website):
    print(f"🔍 Analyzing: {website}")

    text = get_website_text(website)
    social_presence = basic_social_analysis(website)

    prompt = f"""
You are a digital marketing expert.

Analyze this immigration agency website content:

{text}

Social Media Presence:
Facebook: {social_presence['facebook']}
Instagram: {social_presence['instagram']}
YouTube: {social_presence['youtube']}
TikTok: {social_presence['tiktok']}

Give:

1. Website Branding Score (1-10)
2. Social Media Presence Score (1-10)
3. Overall Marketing Score (1-10)
4. Top 5 Marketing Gaps
5. 5 Quick Improvement Tips
6. One strong outreach hook sentence

Be concise and structured.
"""

    ai_output = run_ollama(prompt)
    return ai_output


def main():
    with open("data/leads.csv", newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        leads = list(reader)

    with open("data/scored_leads.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Website",
            "AI Analysis"
        ])

        for lead in leads[:20]:  # limit first test
            website = lead["Website"]

            analysis = analyze_lead(website)

            writer.writerow([website, analysis])

            time.sleep(1)

    print("\n✅ AI Scoring Complete → data/scored_leads.csv")


if __name__ == "__main__":
    main()
