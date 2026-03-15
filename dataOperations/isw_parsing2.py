import os
import re
import csv
from bs4 import BeautifulSoup

folder = "data/isw_raw"
rows = []

def clean_text(text):
    text = re.sub(r'\[\d+\]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

for file in os.listdir(folder):

    if not file.endswith(".html"):
        continue

    with open(os.path.join(folder, file), encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # TITLE
    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else "Unknown"

    # DATE
    date = "Unknown"
    m = re.search(r'\w+ \d{1,2}, \d{4}', title)
    if m:
        date = m.group()

    if title_tag:
        next_p = title_tag.find_next("p")
        if next_p:
            text = next_p.get_text(strip=True)
            m = re.search(r'\w+ \d{1,2}, \d{4}', text)
            if m:
                date = m.group()

    # FULL TEXT
    content = ""
    content_div = soup.find("div", class_="dynamic-entry-content")

    if content_div:

        paragraphs = []

        for p in content_div.find_all("p"):

            text = p.get_text(" ", strip=True)

            if not text:
                continue

            if "Click here" in text:
                continue

            if text.lower().startswith("references"):
                break

            paragraphs.append(clean_text(text))

        content = " ".join(paragraphs)

    rows.append([title, date, content])

with open("isw_reports_full.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["title", "date", "text"])
    writer.writerows(rows)

print("Dataset created:", len(rows))