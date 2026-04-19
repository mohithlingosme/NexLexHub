import json

with open("articles.json", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("TOTAL LINES:", len(lines))