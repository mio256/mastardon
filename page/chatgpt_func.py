import os
import re
import openai
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']


def analyze_toot(mastodon_timelines: list):
    r = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": ''.join([f"id={i.id} - {re.sub(re.compile('<.*?>'), '', i.content)}\n" for i in mastodon_timelines]),
            },
            {
                "role": "system",
                "content": "Pull out sentence about programming from these. You need use this format for response. `{id}, {id}, {id}, {id}, {id}`",
            },
        ]
    )["choices"][0]["message"]["content"]

    l = []
    for x in r.split(','):
        try:
            l.append(int(re.sub(r"\D", "", x)))
        except ValueError:
            pass

    return l, r
