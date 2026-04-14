import datetime as dt
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36"
}

def get_latest_isw_url():
    url = "https://www.understandingwar.org/backgrounder"

    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")

    for link in soup.find_all("a", href=True):
        href = link["href"]

        if "russian-offensive-campaign-assessment" in href:


            if href.startswith("http"):
                return href


            else:
                return "https://www.understandingwar.org" + href

    return None


def get_isw_features():

    date = dt.datetime.now()
    url = get_latest_isw_url()

    if url is None:
        print("ISW link not found")
        return pd.DataFrame()

    print("Using URL:", url)

    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print("Failed to load page")
        return pd.DataFrame()

    soup = BeautifulSoup(response.content, "html.parser")

    paragraphs = soup.find_all("p")
    text = " ".join([p.get_text() for p in paragraphs])

    print("TEXT LENGTH:", len(text))

    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)

    core_words = [
        'russian', 'ukrainian', 'forces', 'ukraine', 'russia',
        'oblast', 'military', 'operations', 'offensive',
        'bakhmut', 'likely', 'war', 'defense',
        'reported', 'claimed', 'stated', 'continued',
        'kremlin', 'putin', 'wagner', 'president',
        'general', 'city', 'donetsk', 'western'
    ]

    data = {'date': [int(date.timestamp())]}

    if len(text.strip()) == 0:
        print("Empty text")
        for w in core_words:
            data[w] = [0.0]
        return pd.DataFrame(data)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix.toarray()[0]

    for w in core_words:
        if w in feature_names:
            idx = list(feature_names).index(w)
            data[w] = [tfidf_scores[idx]]
        else:
            data[w] = [0.0]

    return pd.DataFrame(data)


if __name__ == "__main__":
    df = get_isw_features()
    print(df.head())

    if not df.empty:
        df.to_csv(os.path.join(BASE_DIR, "data", "isw_latest_report.csv"), sep=";", index=False)
        print("Saved to data/isw_latest_report.csv")
