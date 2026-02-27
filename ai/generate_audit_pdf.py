import os
import subprocess
from datetime import datetime

OUTPUT_FOLDER = "reports"

def generate_html(agency_name, website, ai_analysis):
    today = datetime.now().strftime("%d %B %Y")

    html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                padding: 40px;
                color: #222;
            }}
            h1 {{
                color: #0a3d62;
            }}
            .section {{
                margin-top: 20px;
            }}
            .box {{
                background: #f4f6f8;
                padding: 15px;
                border-radius: 8px;
            }}
            .footer {{
                margin-top: 40px;
                font-size: 12px;
                color: #555;
            }}
        </style>
    </head>
    <body>

        <h1>Social Media Growth Audit</h1>
        <p><strong>Agency:</strong> {agency_name}</p>
        <p><strong>Website:</strong> {website}</p>
        <p><strong>Date:</strong> {today}</p>

        <div class="section box">
            <h2>Analysis Summary</h2>
            <pre>{ai_analysis}</pre>
        </div>

        <div class="footer"> Prepared by Digital Growth Consultant<br> Confidential – For Internal Review Only
    </body>
    </html>
    """

    return html_content


def create_pdf(agency_name, html_content):
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    html_file = f"{OUTPUT_FOLDER}/{agency_name}.html"
    pdf_file = f"{OUTPUT_FOLDER}/{agency_name}.pdf"

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    subprocess.run([
        "wkhtmltopdf",
        html_file,
        pdf_file
    ])

    print(f"✅ PDF Generated: {pdf_file}")


def main():
    agency_name = "Advance Visa Consultancy"
    website = "https://advancevisaconsultancy.com"

    ai_analysis = """
Website Branding Score: 4/10
Social Media Score: 3/10
Overall Score: 4/10

Top Gaps:
- Weak CTA
- No consistent content
- Low trust signals

Quick Wins:
1. Add Free Eligibility Form
2. Post 3 reels weekly
3. Showcase student success stories
"""

    html = generate_html(agency_name, website, ai_analysis)
    create_pdf(agency_name.replace(" ", "_"), html)


if __name__ == "__main__":
    main()

