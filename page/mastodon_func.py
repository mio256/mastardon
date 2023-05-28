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

MAX_PAGE = 50


def fetch_me() -> utility.AttribAccessList:
    return mastodon.me()


def toot(text: str) -> None:
    mastodon.toot(text)


def fetch_timeline(max_id: int = None) -> utility.AttribAccessList:
    r = mastodon.timeline_home(max_id=max_id)
    for i, t in enumerate(r):
        r[i]['global_url'] = f'https://mstdn.jp/@{t.account.acct}/{t.id}'
        r[i]['account']['global_url'] = f'https://mstdn.jp/@{t.account.acct}'
    return r


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


def timelines_last(id: str) -> list:
    responses = []
    r = fetch_timeline()
    for _ in range(MAX_PAGE):
        responses += r
        if id in [i.account.id for i in r]:
            break
        r = fetch_timeline(max_id=r[-1].id)
    return responses
