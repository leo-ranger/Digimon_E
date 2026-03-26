import feedparser
import re
import html

# Output file to commit
OUTPUT_FILE = "library.txt"

# Maximum length for article body to avoid freezing in-game
MAX_BODY_LENGTH = 1000

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

#-----------------------------------------------------------------------------
# Function to remove HTML tags and unescape entities
#-----------------------------------------------------------------------------
def strip_html(text):
    if not text:
        return ""
    clean = re.sub(r"<[^>]+>", "", text)  # Remove all HTML tags
    clean = html.unescape(clean)          # Convert &amp;, &nbsp;, &#8230; etc.
    clean = re.sub(r"\s+", " ", clean)    # Collapse multiple whitespace
    return clean.strip()

#-----------------------------------------------------------------------------
# Function to fetch and parse a single RSS feed
#-----------------------------------------------------------------------------
def fetch_rss_entries(url):
    feed = feedparser.parse(url)
    entries = []
    for entry in feed.entries:
        title = strip_html(getattr(entry, 'title', 'No title'))
        desc  = strip_html(getattr(entry, 'summary', ''))
        desc  = desc[:MAX_BODY_LENGTH]  # truncate to avoid freezing
        entries.append({"type": "RNEWS", "title": title, "body": desc})
    return entries

#-----------------------------------------------------------------------------
# Combine all RSS entries
#-----------------------------------------------------------------------------
rnews = []
for url in RSS_URLS:
    rnews.extend(fetch_rss_entries(url))

# Combine all entries (static + RSS)
all_entries = local_lore + digimon_news + rnews

#-----------------------------------------------------------------------------
# Write to library.txt
#-----------------------------------------------------------------------------
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for e in all_entries:
        f.write(f"[LIBRARY {e['type']}]\n")
        f.write(f"Title = {e['title']}\n")
        f.write(f"Body = {e['body']}\n")
        f.write("End = true\n\n")

print(f"Generated {OUTPUT_FILE} with {len(all_entries)} entries.")
