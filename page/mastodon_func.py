import os
import json
from datetime import date, datetime
from mastodon import Mastodon
from dotenv import load_dotenv
load_dotenv()


def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


mastodon = Mastodon(
    os.environ['CLIENT_ID'],
    os.environ['CLIENT_SECRET'],
    os.environ['ACCESS_TOKEN'],
    os.environ['API_BASE_URL'],
)

r = mastodon.timeline_home()
for i in r:
    print(i.account.username)
    print(i.content)

with open('tmp.json', 'w') as f:
    json.dump(r, f, indent=4, default=json_serial)

# TODO: restruct mastodon response
# {
#     "id": 110350116606473858,
#     "created_at": "2023-05-11T12:45:52.320000+00:00",
#     "url": "https://mastodon.compositecomputer.club/@hanya/110350116606473858",
#     "replies_count": 0,
#     "reblogs_count": 1,
#     "favourites_count": 1,
#     "content": "<p>\u306a\u3093\u3067Oauth2\u306f\u901a\u308b\u306e\u306bSECRET_KEY\u306f\u901a\u3089\u306a\u3044\u3093\u3060\u3068\u601d\u3063\u30662\u65e5\u304f\u3089\u3044\u60a9\u3093\u3067\u305f\u3093\u3060\u3051\u3069\u3001\u74b0\u5883\u5909\u6570\u304c\u7af6\u5408\u3057\u3066\u305f\u3002</p>",
#     "account": {
#         "id": 110338197845675853,
#         "username": "hanya",
#         "display_name": "\u306f\u306b\u3083",
#         "url": "https://mastodon.compositecomputer.club/@hanya",
#         "avatar": "https://s3.ap-northeast-1.wasabisys.com/mastodondb/accounts/avatars/110/338/197/845/675/853/original/9b8ad9d0b552f87d.png"
#     }
# },
