import feedparser

# Output file to commit
OUTPUT_FILE = "library.txt"

# Digimon LORE and DNEWS - can be static entries
local_lore = [
    {"type": "LORE", "title": "New Aquatic Digimon", "body": "A single-eyed fish Digimon has appeared in deep network zones."},
]

digimon_news = [
    {"type": "DNEWS", "title": "Digital Storm Warning", "body": "Network turbulence detected across the eastern sector."},
]

# Fetch ABC News RSS
RSS_URL = "https://www.abc.net.au/news/feed/104217382/rss.xml"
feed = feedparser.parse(RSS_URL)

rnews = []
for entry in feed.entries:
    title = entry.title.replace("\n", " ").strip()
    desc = entry.summary.replace("\n", " ").strip() if "summary" in entry else ""
    rnews.append({"type": "RNEWS", "title": title, "body": desc})

# Combine all entries
all_entries = local_lore + digimon_news + rnews

# Write to library.txt
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for e in all_entries:
        f.write(f"[LIBRARY {e['type']}]\n")
        f.write(f"Title = {e['title']}\n")
        f.write(f"Body = {e['body']}\n")
        f.write("End = true\n\n")

print(f"Generated {OUTPUT_FILE} with {len(all_entries)} entries.")
