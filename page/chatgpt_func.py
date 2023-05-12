import os
import re
import openai
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']


def analyze_toot(mastodon_timelines: list):
    messages = [
        {
            "role": "system",
            "content": """
                Analyze the tweets and arrange them in order of relevance to programming.
                The format for responses is below.
                DON'T send response outside of the format, as it crash the program.
                ```
                {id}, {id}, {id}, {id}, {id}
                ```
                """
        },
    ]
    for i in mastodon_timelines:
        messages.append({
            "role": "user",
            "content": f"id={i.id}\n {i.content}"
        })
    r = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )["choices"][0]["message"]["content"].split(',')
    # print(res)

    l = []
    for x in r:
        x = re.sub(r"\D", "", x)
        try:
            l.append(int(x))
        except ValueError:
            pass
    # print(l)

    return l
