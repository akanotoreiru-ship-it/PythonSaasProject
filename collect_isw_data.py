import requests
import time
from datetime import datetime, timedelta
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

OUTPUT_FOLDER = Path("data/isw_raw")
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (research bot for academic purposes)"
}

session = requests.Session()
session.headers.update(HEADERS)

def generate_dates(start, end):
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)


def generate_urls(date):
    """Return possible ISW URLs for a given date"""

    urls = []

    # Old ISW format
    urls.append(
        f"https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-{date.strftime('%B-%d').replace('-0','-').lower()}"
    )

    # Short link format
    urls.append(
        f"https://isw.pub/UkrWar{date.strftime('%m%d%y')}"
    )

    # Early war reports format
    urls.append(
        f"https://www.understandingwar.org/backgrounder/russia-ukraine-warning-update-russian-offensive-campaign-assessment-{date.strftime('%B-%d-%Y').lower()}"
    )

    return urls


def download_page(date):

    file_name = date.strftime("%Y_%m_%d") + ".html"
    file_path = OUTPUT_FOLDER / file_name

    if file_path.exists():
        return f"SKIP {file_name}"

    urls = generate_urls(date)

    for url in urls:
        try:
            r = session.get(url, timeout=15)

            if r.status_code == 200 and len(r.text) > 5000:

                with open(file_path, "wb") as f:
                    f.write(r.content)

                return f"OK {date.date()}"

        except Exception as e:
            continue

    return f"FAIL {date.date()}"


def main():

    start = datetime(2022,2,24)
    end = datetime(2026,3,1)

    dates = list(generate_dates(start, end))

    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(download_page, dates)

        for r in results:
            print(r)


if __name__ == "__main__":
    main()