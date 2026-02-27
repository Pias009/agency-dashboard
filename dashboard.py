from flask import Flask
import csv
import os
import urllib.parse

app = Flask(__name__)

DATA_FILE = "data/master_leads.csv"
AUDIT_FOLDER = "reports/png"


def load_master_leads():
    leads = []

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                leads.append(row)

    return leads


def generate_whatsapp_link(phone):
    message = """
Assalamu Alaikum,

I reviewed your agency’s online presence and found opportunities to increase qualified student inquiries.

If you're open, I can share a short improvement summary.
"""
    encoded = urllib.parse.quote(message)
    clean_phone = phone.replace("+", "").replace(" ", "")
    return f"https://wa.me/{clean_phone}?text={encoded}"


def generate_safe_name(url):
    if not url:
        return ""
    safe = url.replace("https://", "").replace("http://", "")
    safe = safe.replace("/", "").replace(".", "_")
    return safe


@app.route("/")
def home():
    leads = load_master_leads()
    total = len(leads)

    html = f"""
    <html>
    <head>
        <title>🚀 Live Lead Dashboard</title>
        <meta http-equiv="refresh" content="5">
        <style>
            body {{
                font-family: Arial;
                padding: 20px;
                background: #f4f6f8;
            }}
            h2 {{
                color: #0A3D62;
            }}
            .counter {{
                background: #0A3D62;
                color: white;
                padding: 10px 15px;
                display: inline-block;
                margin-bottom: 20px;
                border-radius: 6px;
                font-weight: bold;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                background: white;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                font-size: 13px;
                text-align: left;
            }}
            th {{
                background-color: #0A3D62;
                color: white;
            }}
            a {{
                text-decoration: none;
                color: #0A3D62;
            }}
            .btn {{
                background-color: #25D366;
                color: white;
                padding: 6px 10px;
                border-radius: 4px;
                font-size: 12px;
                text-decoration: none;
                display: inline-block;
            }}
            .audit-btn {{
                background-color: #0A3D62;
                color: white;
                padding: 6px 10px;
                border-radius: 4px;
                font-size: 12px;
                text-decoration: none;
                display: inline-block;
            }}
        </style>
    </head>
    <body>

    <h2>🚀 Live Lead Dashboard</h2>
    <div class="counter">Total Leads: {total}</div>

    <table>
        <tr>
            <th>Source</th>
            <th>Website</th>
            <th>Facebook</th>
            <th>Phone</th>
            <th>Email</th>
            <th>Audit</th>
            <th>Ads</th>
            <th>WhatsApp</th>
        </tr>
    """

    for lead in leads:
        source = lead.get("Source", "")
        website = lead.get("Website", "")
        facebook = lead.get("Facebook", "")
        phone = lead.get("Phone", "")
        email = lead.get("Email", "")

        base_url = website if website else facebook
        safe_name = generate_safe_name(base_url)
        audit_file = f"{AUDIT_FOLDER}/{safe_name}.png"

        if os.path.exists(audit_file):
            audit_btn = f'<a class="audit-btn" target="_blank" href="/{audit_file}">View Audit</a>'
        else:
            audit_btn = "N/A"

        # Ads Library Link
        if facebook:
            page_identifier = facebook.rstrip("/").split("/")[-1]
            ads_link = f"https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=BD&q={page_identifier}"
            ads_btn = f'<a class="audit-btn" target="_blank" href="{ads_link}">Check Ads</a>'
        else:
            ads_btn = "N/A"

        # WhatsApp Button
        if phone:
            wa_link = generate_whatsapp_link(phone)
            wa_btn = f'<a class="btn" target="_blank" href="{wa_link}">WhatsApp</a>'
        else:
            wa_btn = "N/A"

        html += f"""
        <tr>
            <td>{source}</td>
            <td><a href="{website}" target="_blank">{website}</a></td>
            <td><a href="{facebook}" target="_blank">{facebook}</a></td>
            <td>{phone}</td>
            <td>{email}</td>
            <td>{audit_btn}</td>
            <td>{ads_btn}</td>
            <td>{wa_btn}</td>
        </tr>
        """

    html += """
    </table>

    </body>
    </html>
    """

    return html


if __name__ == "__main__":
    app.run()
