import feedparser
import re

# Output file to commit
OUTPUT_FILE = "library.txt"

# Digimon LORE and DNEWS - static entries
local_lore = [
    {"type": "LORE", "title": "New Aquatic Digimon", "body": "A single-eyed fish Digimon has appeared in deep network zones."},
]

digimon_news = [
    {"type": "DNEWS", "title": "Digital Storm Warning", "body": "Network turbulence detected across the eastern sector."},
]

# List of RSS feeds to fetch
RSS_URLS = [
    "https://www.abc.net.au/news/feed/104217382/rss.xml",
    "https://withthewill.net/forums/-/index.rss",
    # Add more RSS URLs here
]

# Function to remove HTML tags
def strip_html(text):
    clean = re.sub(r"<[^>]+>", "", text)  # Remove tags like <div>, <p>, <br>
    clean = re.sub(r"&nbsp;|&amp;|&lt;|&gt;", " ", clean)  # Replace common HTML entities
    clean = clean.replace("\n", " ").strip()
    return clean

# Function to fetch and parse a single RSS feed
def fetch_rss_entries(url):
    feed = feedparser.parse(url)
    entries = []
    for entry in feed.entries:
        title = strip_html(entry.title)
        desc = strip_html(entry.summary) if "summary" in entry else ""
        entries.append({"type": "RNEWS", "title": title, "body": desc})
    return entries

# Combine all RSS entries
rnews = []
for url in RSS_URLS:
    rnews.extend(fetch_rss_entries(url))

# Combine all entries (static + RSS)
all_entries = local_lore + digimon_news + rnews

# Write to library.txt
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for e in all_entries:
        f.write(f"[LIBRARY {e['type']}]\n")
        f.write(f"Title = {e['title']}\n")
        f.write(f"Body = {e['body']}\n")
        f.write("End = true\n\n")

print(f"Generated {OUTPUT_FILE} with {len(all_entries)} entries.")
