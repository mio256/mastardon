import os
import re
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']


def analyze_toots(mastodon_timelines: list) -> tuple[list[int], str]:
    """
    Analyzes toots using GPT-3.5-turbo and returns a list of relevant toot IDs and GPT-3's response.

    :param mastodon_timelines: A list of Mastodon timeline objects.
    :return: A tuple containing a list of relevant toot IDs and GPT-3's response.
    """
    message_content = ''.join([f"id={toot.id} - {re.sub(re.compile('<.*?>'), '', toot.content)}\n" for toot in mastodon_timelines])

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": message_content},
            {
                "role": "system",
                "content": "Pull out sentences about programming from these. You need to use this format for response. `{id}, {id}, {id}, {id}, {id}`",
            },
        ]
    )["choices"][0]["message"]["content"]

    relevant_toot_ids = [int(re.sub(r"\D", "", id)) for id in response.split(',') if re.search(r"\d", id)]

    return relevant_toot_ids, response
