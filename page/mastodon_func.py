import os
from mastodon import Mastodon
from dotenv import load_dotenv
load_dotenv()


def timelines(page: int = 5):
    mastodon = Mastodon(
        os.environ['CLIENT_ID'],
        os.environ['CLIENT_SECRET'],
        os.environ['ACCESS_TOKEN'],
        os.environ['API_BASE_URL'],
    )

    responses = []
    r = mastodon.timeline_home()
    for _ in range(page):
        responses += r
        r = mastodon.timeline_home(max_id=r[-1].id)
    return responses
