import json
import os

meeting_words = [
    "hello",
    "thank you",
    "yes",
    "no",
    "question",
    "understand",
    "agree",
    "next",
    "problem",
    "ok"
]

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load the WLASL dataset
wlasl_path = os.path.join(script_dir, "WLASL_v0.3.json")
with open(wlasl_path, "r") as f:
    wlasl_data = json.load(f)

# Filter objects where gloss matches meeting words
filtered_data = []
for obj in wlasl_data:
    gloss = obj.get("gloss", "")
    if gloss in meeting_words:
        filtered_data.append(obj)

# Write filtered data to wlasl_subset.json
output_path = os.path.join(script_dir, "wlasl_subset.json")
with open(output_path, "w") as f:
    json.dump(filtered_data, f, indent=4)

print(f"Filtered {len(filtered_data)} objects from {len(wlasl_data)} total objects")

