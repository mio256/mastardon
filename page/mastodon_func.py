import os
import datetime
from mastodon import Mastodon
from dotenv import load_dotenv
load_dotenv()

mastodon = Mastodon(
    os.environ['CLIENT_ID'],
    os.environ['CLIENT_SECRET'],
    os.environ['ACCESS_TOKEN'],
    os.environ['API_BASE_URL'],
)


def timelines_page(page: int):
    responses = []
    r = mastodon.timeline_home()
    for _ in range(page):
        responses += r
        r = mastodon.timeline_home(max_id=r[-1].id)
    return responses


def timelines_hours(hours: int):
    d = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=hours)
    responses = []

    r = mastodon.timeline_home()
    responses += r
    while r[-1].created_at > d:
        r = mastodon.timeline_home(max_id=r[-1].id)
        responses += r

    return responses
