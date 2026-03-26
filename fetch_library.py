import feedparser
import re
import html

# Output file
OUTPUT_FILE = "library.txt"

# Digimon LORE and DNEWS - static entries
local_lore = [
    {"type": "LORE", "title": "New Aquatic Digimon", "body": "A single-eyed fish Digimon has appeared in deep network zones."},
]

digimon_news = [
    {"type": "DNEWS", "title": "Digital Storm Warning", "body": "Network turbulence detected across the eastern sector."},
]

# List of RSS feeds
RSS_URLS = [
    "https://www.abc.net.au/news/feed/104217382/rss.xml",
    "https://withthewill.net/forums/-/index.rss",
    # Add more RSS URLs here
]

#----------------------------
# Clean and shorten text
#----------------------------
def clean_text(text):
    if not text:
        return ""
    # Remove HTML tags
    text = re.sub(r"<[^>]+>", "", text)
    # Convert HTML entities to actual characters
    text = html.unescape(text)
    # Remove zero-width spaces and other invisible chars
    text = re.sub(r"[\u200B-\u200D\uFEFF]", "", text)
    # Remove trailing "Read more" and replace with [...]
    text = re.sub(r"\s*read more\.{0,3}", " [...]", text, flags=re.IGNORECASE)
    # Find first date/time pattern and cut everything after it
    date_time_pattern = re.compile(
        r"(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),?\s+\w+\s+\d{1,2}(?:st|nd|rd|th)?|"  # Dates
        r"\d{1,2}:\d{2}\s*(?:am|pm)|"  # Times
        r"\(\w+\)"  # Timezones
        , flags=re.IGNORECASE
    )
    match = date_time_pattern.search(text)
    if match:
        text = text[:match.start()].strip()
        # Remove trailing punctuation like ":" or "-" if left dangling
        text = re.sub(r"[:\-]+$", "", text).strip()
    # Collapse multiple whitespace into a single space
    text = re.sub(r"\s+", " ", text)
    return text

#----------------------------
# Fetch a single RSS feed
#----------------------------
def fetch_rss_entries(url, max_articles=5):
    feed = feedparser.parse(url)
    entries = []
    for entry in feed.entries[:max_articles]:
        title = clean_text(entry.title)
        desc = clean_text(entry.summary) if "summary" in entry else ""
        entries.append({"type": "RNEWS", "title": title, "body": desc})
    return entries

#----------------------------
# Combine all RSS entries
#----------------------------
rnews = []
for url in RSS_URLS:
    rnews.extend(fetch_rss_entries(url, max_articles=5))

# Combine static entries + RSS
all_entries = local_lore + digimon_news + rnews

#----------------------------
# Write to library.txt
#----------------------------
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for e in all_entries:
        f.write(f"[LIBRARY {e['type']}]\n")
        f.write(f"Title = {e['title']}\n")
        f.write(f"Body = {e['body']}\n")
        f.write("End = true\n\n")

print(f"Generated {OUTPUT_FILE} with {len(all_entries)} entries.")
