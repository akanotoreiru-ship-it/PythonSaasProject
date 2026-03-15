import os
import csv
import re
from bs4 import BeautifulSoup

folder = "data/isw_raw"

rows = []
idx = 1

for file in os.listdir(folder):

    if not file.endswith(".html"):
        continue

    path = os.path.join(folder, file)

    with open(path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # TITLE
    title = "Unknown"
    h1 = soup.find("h1")
    if h1:
        title = h1.get_text(strip=True)

    # DATE
    date = "Unknown"
    text = soup.get_text(" ")

    m = re.search(r'\w+ \d{1,2}, \d{4}', text)
    if m:
        date = m.group()

    summary = "Unknown"

    for p in soup.find_all("p"):

        t = p.get_text(" ", strip=True)

        if len(t) > 120:   # щоб не брати короткі підписи
            summary = t
            break

    rows.append([idx, title, date, summary])
    idx += 1


with open("isw_dataset.csv", "w", newline="", encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow(["id", "title", "date", "summary"])
    writer.writerows(rows)

print("Done. Parsed:", len(rows), "reports")