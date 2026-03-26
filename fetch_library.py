import feedparser
import re
from html import unescape

# Output file
OUTPUT_FILE = "library.txt"

# Digimon LORE and DNEWS - static entries
local_lore = [
    {"type": "LORE", "title": "New Aquatic Digimon", "body": "A single-eyed fish Digimon has appeared in deep network zones."},
]

digimon_news = [
    {"type": "DNEWS", "title": "Digital Storm Warning", "body": "Network turbulence detected across the eastern sector."},
]

# RSS feeds to fetch
RSS_URLS = [
    "https://www.abc.net.au/news/feed/104217382/rss.xml",
    "https://withthewill.net/forums/-/index.rss",
]

MAX_ARTICLES_PER_FEED = 5
MIN_BODY_LENGTH = 50  # minimum body length

# ---------------------------
# Utility functions
# ---------------------------

def strip_html(text):
    """Remove HTML tags and normalize common HTML entities"""
    text = re.sub(r"<[^>]+>", "", text)  # remove tags
    text = unescape(text)  # decode entities like &#039;
    text = re.sub(r"&nbsp;|&amp;|&lt;|&gt;", " ", text)
    text = text.replace("\n", " ")
    return text

def normalize_text(text):
    """Clean up spacing, zero-width chars, and unwanted sequences"""
    text = re.sub(r'[\u200b\u200c\u200d]+', '', text)  # remove zero-width chars
    text = re.sub(r'\s+', ' ', text)  # collapse multiple spaces/tabs/newlines
    # Remove extra times/dates often found in simulcast text
    text = re.sub(r'expected at:.*', '', text, flags=re.IGNORECASE)
    text = re.sub(r"If your time isn't included.*", '', text, flags=re.IGNORECASE)
    # Replace Read more variations with [...]
    text = re.sub(r'\s*Read more\.{0,3}', ' [...]', text, flags=re.IGNORECASE)
    return text.strip()

def extract_first_sentences(text, n=2):
    """Keep first n sentences for brevity"""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return " ".join(sentences[:n]).strip()

def clean_body(text):
    """Full cleaning pipeline"""
    if not text:
        return "[...]"
    text = strip_html(text)
    text = normalize_text(text)
    text = extract_first_sentences(text, n=2)
    if len(text) < MIN_BODY_LENGTH:
        text += " [...]"
    return text

# ---------------------------
# Fetch RSS entries
# ---------------------------

def fetch_rss_entries(url):
    feed = feedparser.parse(url)
    entries = []
    for entry in feed.entries[:MAX_ARTICLES_PER_FEED]:  # top N articles only
        title = clean_body(entry.title)
        desc = clean_body(entry.summary) if "summary" in entry else ""
        entries.append({"type": "RNEWS", "title": title, "body": desc})
    return entries

# ---------------------------
# Combine all entries
# ---------------------------

rnews = []
for url in RSS_URLS:
    rnews.extend(fetch_rss_entries(url))

all_entries = local_lore + digimon_news + rnews

# ---------------------------
# Write to library.txt
# ---------------------------

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for e in all_entries:
        f.write(f"[LIBRARY {e['type']}]\n")
        f.write(f"Title = {e['title']}\n")
        f.write(f"Body = {e['body']}\n")
        f.write("End = true\n\n")

print(f"Generated {OUTPUT_FILE} with {len(all_entries)} entries.")
