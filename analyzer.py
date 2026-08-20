import anthropic
import os
import argparse
import sqlite3
from flask import Flask


connection = sqlite3.connect("threats.db")
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS threats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    threat_type TEXT,
    description TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

connection.commit()
cursor.close()

parser = argparse.ArgumentParser()
parser.add_argument("--log-file", default="sample.log")
args = parser.parse_args()

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def analyze_logs(log_file):
    with open(log_file, "r") as f:
        log_content = f.read()

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": f"Analyze these security logs and identify threats:\n\n{log_content}"}
        ]
    )

    return message.content[0].text

def send_alert(message):
    gmail_api_key = os.environ.get("GMAIL_API_KEY")
    if not gmail_api_key:
        print("GMAIL_API_KEY not set. Cannot send alert.")
        return
    
def save_database(threat_type, description):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO threats (threat_type, description) VALUES (?, ?)", (threat_type, description))
    connection.commit()
    cursor.close()



result = analyze_logs(args.log_file)
send_alert(result)
save_database("Threat Analysis", result)

print(result)
with open("report.md", "w") as f:
    f.write(result)

print("Analysis report saved to report.md")