import os
import re
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']


def request_chatgpt(messages: list):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )


def analyze_toots(mastodon_timelines: list) -> tuple[list[int], str]:
    message_content = ''.join([f"id={toot.id} - {re.sub(re.compile('<.*?>'), '', toot.content)}\n" for toot in mastodon_timelines])

    response = request_chatgpt(
        messages=[
            {"role": "user", "content": message_content},
            {
                "role": "system",
                "content": """
                    You are a professional analyst.
                    Please output `id list of statements about programming` based on the following constraints and input statements.
                    # Constraints
                     - Output no more than 20 IDs.
                     - Use this format for output : `{id}, {id}, {id}, {id}, {id}`
                    I'll send you the input data.
                """,
            },
        ]
    )["choices"][0]["message"]["content"]

    relevant_toot_ids = [int(re.sub(r"\D", "", id)) for id in response.split(',') if re.search(r"\d", id)]

    return relevant_toot_ids, response
