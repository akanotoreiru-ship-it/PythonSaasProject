import asyncio
from telethon import TelegramClient
import pandas as pd

api_id = <own id for API>
api_hash = '<own api_hash>'
channel_username = '<your choice for telegram channel>'

keywords = [
    'Україна',
    'Ukraine',
    'війна',
    'war',
    'ЗСУ',
    'Russia',
    'Росія',
    'приліт',
    'вибух',
    'ціль'
]
#keywords can be also selected by yourself


async def main():
    data = []

    async with TelegramClient('session', api_id, api_hash) as client:

        async for message in client.iter_messages(channel_username, limit=5000):

            if message.text:
                if any(word.lower() in message.text.lower() for word in keywords):
                    data.append({
                        'date': message.date,
                        'text': message.text,
                        'views': message.views,
                        'forwards': message.forwards,
                        'replies': message.replies.replies if message.replies else None
                    })

    df = pd.DataFrame(data)
    df.to_csv('<given name for parsed dataset>', index=False)
    print("Збережено", len(df), "постів")


asyncio.run(main())