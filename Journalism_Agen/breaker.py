import json

chunk_size = 500
chunk = []
file_index = 0

with open("articles.json", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        
        try:
            obj = json.loads(line)
            chunk.append(obj)
        except json.JSONDecodeError:
            print("Skipping bad line")
            continue

        if len(chunk) >= chunk_size:
            with open(f"chunk_{file_index}.json", "w", encoding="utf-8") as out:
                json.dump(chunk, out, ensure_ascii=False, indent=2)
            chunk = []
            file_index += 1

# save remaining
if chunk:
    with open(f"chunk_{file_index}.json", "w", encoding="utf-8") as out:
        json.dump(chunk, out, ensure_ascii=False, indent=2)
        