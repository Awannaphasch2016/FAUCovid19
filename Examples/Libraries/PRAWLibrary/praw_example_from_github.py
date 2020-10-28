import praw

from credentials import REDDIT_CLIENT_ID
from credentials import REDDIT_CLIENT_SECRET
from credentials import REDDIT_PASSWORD
from credentials import REDDIT_USERNAME
# client_id
# client_secret
# user_agent
from credentials import REDDIT_USER_AGENT

reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                     client_secret=REDDIT_CLIENT_SECRET,
                     password=REDDIT_PASSWORD,
                     user_agent=REDDIT_USER_AGENT,
                     username=REDDIT_USERNAME)

x = reddit.subreddit("test").submit("Test Submission",
                                    url="https://reddit.com")
print(x)
