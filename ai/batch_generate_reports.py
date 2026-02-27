import csv
import os
import re
import subprocess
from datetime import datetime

HTML_FOLDER = "reports/html"
PNG_FOLDER = "reports/png"

def extract_scores(text):
    website = re.search(r'Website.*?(\d+)/10', text)
    social = re.search(r'Social.*?(\d+)/10', text)
    overall = re.search(r'Overall.*?(\d+)/10', text)

    return {
        "website": website.group(1) if website else "5",
        "social": social.group(1) if social else "5",
        "overall": overall.group(1) if overall else "5"
    }

def extract_bullet_points(section_name, text):
    section = re.search(rf'{section_name}.*?:([\s\S]*?)(\n\n|\Z)', text)
    if section:
        lines = section.group(1).split("\n")
        clean = [l.strip("-• ").strip() for l in lines if l.strip()]
        return clean[:4]
    return []

def generate_html(agency_name, website, scores, gaps, tips):
    today = datetime.now().strftime("%d %B %Y")

    return f"""
    <html>
    <head>
    <style>
        body {{
            font-family: Arial;
            padding: 40px;
            background: #ffffff;
        }}
        h1 {{ color: #0A3D62; }}
        .score-box {{
            display:inline-block;
            width:30%;
            background:#f4f6f8;
            padding:15px;
            margin-right:10px;
            border-radius:8px;
            text-align:center;
            font-weight:bold;
        }}
        ul {{ line-height:1.6; }}
        .section {{ margin-top:30px; }}
    </style>
    </head>
    <body>

    <h1>Social Media Growth Audit</h1>
    <p><strong>Agency:</strong> {agency_name}<br>
    <strong>Website:</strong> {website}<br>
    <strong>Date:</strong> {today}</p>

    <div>
        <div class="score-box">Website: {scores['website']}/10</div>
        <div class="score-box">Social: {scores['social']}/10</div>
        <div class="score-box">Overall: {scores['overall']}/10</div>
    </div>

    <div class="section">
        <h2>Key Growth Gaps</h2>
        <ul>
        {''.join(f'<li>{g}</li>' for g in gaps)}
        </ul>
    </div>

    <div class="section">
        <h2>Quick Wins</h2>
        <ul>
        {''.join(f'<li>{t}</li>' for t in tips)}
        </ul>
    </div>

    </body>
    </html>
    """

def save_png(agency_name, html_content):
    if not os.path.exists(HTML_FOLDER):
        os.makedirs(HTML_FOLDER)
    if not os.path.exists(PNG_FOLDER):
        os.makedirs(PNG_FOLDER)

    safe_name = agency_name.replace(" ", "_")
    html_path = f"{HTML_FOLDER}/{safe_name}.html"
    png_path = f"{PNG_FOLDER}/{safe_name}.png"

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    subprocess.run(["wkhtmltoimage", html_path, png_path])

    print(f"✅ Generated: {png_path}")

def main():
    with open("data/scored_leads.csv", newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            website = row["Website"]
            analysis = row["AI Analysis"]

            agency_name = website.replace("https://", "").replace("http://", "").split("/")[0]

            scores = extract_scores(analysis)
            gaps = extract_bullet_points("Gaps", analysis)
            tips = extract_bullet_points("Quick", analysis)

            if not gaps:
                gaps = ["Weak CTA", "Low engagement", "No clear funnel"]

            if not tips:
                tips = ["Add Free Consultation CTA", "Post 3 reels weekly", "Showcase testimonials"]

            html = generate_html(agency_name, website, scores, gaps, tips)
            save_png(agency_name, html)

if __name__ == "__main__":
 main()
