# Telegram Data Parser

Python script for parsing public Telegram channels and extracting posts related to the topic.

## Features

* Parses messages from public Telegram channels
* Filters posts by keywords (Ukraine, war, etc.)
* Saves data to CSV
* Collects views, forwards, and replies count

## Installation

```bash
git clone https://github.com/akanotoreiru-ship-it/tg_parser.py.git
cd telegram-war-parser
pip install -r requirements.txt
```

## Usage

1. Get your API credentials from official telegram resource.

2. Open `tg_parsing.py` and set:

   * api_id
   * api_hash
   * channel username

3. Run the script:

```bash
python tg_parsing.py
```

4. Enter your phone number in international format:

```
+XXXXXXXXXXXX
```

5. Enter the code sent via Telegram

## Output

CSV file with parsed posts:

* date
* text
* views
* forwards
* replies

## Notes

* Works only with public channels
* Session file is created automatically
* Do NOT share your API hash or session file
