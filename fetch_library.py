import feedparser
import re
from html import unescape

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

MAX_ARTICLES_PER_FEED = 5
MIN_BODY_LENGTH = 50  # minimum length for an article body

# Function to remove HTML tags
def strip_html(text):
    text = re.sub(r"<[^>]+>", "", text)  # Remove tags like <div>, <p>, <br>
    text = re.sub(r"&nbsp;|&amp;|&lt;|&gt;", " ", text)  # Replace common HTML entities
    text = text.replace("\n", " ").strip()
    return text

# Keep only the first 1-2 sentences
def extract_first_sentences(text, n=2):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return " ".join(sentences[:n]).strip()

# Clean and normalize article body
def clean_body(text):
    text = strip_html(text)
    text = unescape(text)  # converts &#039; → ', etc.
    text = re.sub(r'\u200b+', '', text)  # remove zero-width chars
    text = re.sub(r'\s+Read more\.{0,3}', ' [...]', text, flags=re.IGNORECASE)  # replace "Read more..."
    text = extract_first_sentences(text, n=2)  # keep first 1-2 sentences
    if len(text) < MIN_BODY_LENGTH:
        text += " [...]"
    return text

# Fetch and parse a single RSS feed
def fetch_rss_entries(url):
    feed = feedparser.parse(url)
    entries = []
    for entry in feed.entries[:MAX_ARTICLES_PER_FEED]:  # limit top N articles
        title = clean_body(entry.title)
        desc = clean_body(entry.summary) if "summary" in entry else ""
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
