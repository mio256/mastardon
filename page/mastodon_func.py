import os
import datetime
from mastodon import Mastodon, utility
from dotenv import load_dotenv

load_dotenv()

mastodon = Mastodon(
    os.environ['CLIENT_ID'],
    os.environ['CLIENT_SECRET'],
    os.environ['ACCESS_TOKEN'],
    os.environ['API_BASE_URL'],
)


def fetch_timeline(max_id: int = None) -> utility.AttribAccessList:
    return mastodon.timeline_home(max_id=max_id)


def timelines_page(page: int) -> list:
    responses = []
    r = fetch_timeline()
    for _ in range(page):
        responses += r
        r = fetch_timeline(max_id=r[-1].id)
    return responses


def timelines_hours(hours: int) -> list:
    d = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=hours)
    responses = []
    r = fetch_timeline()
    responses += r
    while r[-1].created_at > d:
        r = fetch_timeline(max_id=r[-1].id)
        responses += r
    return responses
