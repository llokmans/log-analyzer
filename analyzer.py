import anthropic
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--log-file", default="sample.log")
args = parser.parse_args()

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

with open(args.log_file, "r") as f:
    log_content = f.read()

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": f"Analyze these security logs and identify threats:\n\n{log_content}"}
    ]
)

print(message.content[0].text)

with open("report.md", "w") as f:
    f.write(message.content[0].text)
    
print("Analysis report saved to report.md")