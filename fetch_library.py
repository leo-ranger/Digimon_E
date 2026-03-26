import feedparser
import re
import html

# Output file to commit
OUTPUT_FILE = "library.txt"

# Maximum length for article body to avoid freezing in-game
MAX_BODY_LENGTH = 1000

# Maximum number of articles per RSS feed
MAX_ARTICLES_PER_FEED = 5

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
]

#-----------------------------------------------------------------------------
# Function to clean HTML, convert entities, remove zero-width chars
#-----------------------------------------------------------------------------
def clean_text(text):
    if not text:
        return ""
    # Remove HTML tags
    text = re.sub(r"<[^>]+>", "", text)
    # Convert HTML entities to actual characters
    text = html.unescape(text)
    # Remove zero-width spaces and other invisible chars
    text = re.sub(r"[\u200B-\u200D\uFEFF]", "", text)
    # Collapse multiple whitespace into a single space
    text = re.sub(r"\s+", " ", text)
    return text.strip()

#-----------------------------------------------------------------------------
# Fetch and parse RSS feed (top N articles)
#-----------------------------------------------------------------------------
def fetch_rss_entries(url, max_articles=MAX_ARTICLES_PER_FEED):
    feed = feedparser.parse(url)
    entries = []
    for entry in feed.entries[:max_articles]:
        title = clean_text(getattr(entry, 'title', 'No title'))
        desc  = clean_text(getattr(entry, 'summary', ''))
        desc  = desc[:MAX_BODY_LENGTH]  # truncate to prevent freezing
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
