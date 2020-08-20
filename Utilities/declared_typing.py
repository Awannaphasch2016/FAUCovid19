import datetime
import json
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple

from typing_extensions import Literal
from typing_extensions import TypedDict
# RunningConditions = Dict[str, str]

Url = str
RedditAggs = Dict
TwitterAggs = Dict

Json = Dict
Tags = Optional[Tuple[str]]
Query = Optional[List[str]]
Crawler_type = str

# res = {'a': 1}
# r = json.dumps(res)
# y = json.loads(r)
# Json = type(y)

Frequency = Literal['day']
Sort = Literal['asc', 'desc']
epoch_datetime = int

class TwitterCollectionkey(TypedDict):
    aspect: List[str]
    query: Query

class TwitterCollection(TypedDict):
    collection: TwitterCollectionkey
    name: str

class SubredditCollectionKey(TypedDict):
    subreddit: List[str]
    query: Query

class SubredditCollection(TypedDict):
    collection: SubredditCollectionKey
    name: str

class RedditRunningConstraints(TypedDict):
    aggs: Optional[str]
    after: int
    before: Optional[int]
    size: int
    metadata: str
    sort: Sort
    # fields: str
#

class TwitterRunningConstraints(TypedDict):
    aggs: Optional[str]
    after: int
    before: Optional[int]
    size: Optional[int]  # None = all
    metadata: str
    sort: Sort
    fields: Optional[str]  # None = all



class RunningConditions(TypedDict):
    crawler_option: str
    collection_name: str
    respond_type: str
    search_type: str
    sort: Sort
    tag: Optional[str]
    max_after: int

RunningConditionsKeyValue = List[Tuple[List[str], RunningConditions]]

class RedditMetadata(TypedDict):
    running_constraints: RedditRunningConstraints
    after: str
    agg_size: int
    aggs: List[str]
    before: Optional[str]
    execution_time_milliseconds: float
    frequency: Frequency
    index: str
    results_returned: int
    size: int
    sort: Sort
    subreddit: List[str]
    total_results: int
    fields: List[str]


class TwitterMetadata(TypedDict):
    running_constraints: TwitterRunningConstraints
    after: str
    aggs: List[str]
    before: Optional[str]
    execution_time_milliseconds: float
    frequency: Frequency
    results_returned: int
    size: int
    sort: Sort
    timed_out: bool
    search_words: List[str]
    total_results: int
    fields: List[str]


class RedditData(TypedDict):
    # common_fields
    author: str
    author_flair_richtext: Optional[str]
    author_flair_type: Optional['str']
    author_fullname: str
    id: str
    created_utc: epoch_datetime
    permalink: str
    retrieved_on: epoch_datetime
    score: int
    subreddit: str
    subreddit_id: str
    total_awards_received: int
    stickied: bool
    all_awardings: List[str]

    # subreddit_fields
    domain: str
    full_link: Url
    is_original_content: bool
    is_self: bool
    num_comments: int
    pinned: bool
    selftext: str
    subreddit_subscribers: int
    title: str
    upvote_ratio: Optional[float]

    # comment fields
    body: str
    parent_id: str
    link_id: str

    # Added later
    sentiment_polarity: float


class TwitterData(TypedDict):
    author_fullname: str #to author_fullname
    to: Optional[str]
    body: str # body
    retweets: int
    favorites: int # to score
    replies: int
    id: str
    premalink: str
    author_id: int
    created_utc: epoch_datetime # to craeted_ utc
    formatted_date: str
    hashtags: str
    mentions: str
    geo: str
    full_link: Url # to full_linh
    retrieved_on: epoch_datetime

    # Added later
    sentiment_polarity: float


class RedditResponse(TypedDict):
    data: List[RedditData]
    metadata: List[RedditMetadata]
    aggs: List[RedditAggs]


class TwitterResponse(TypedDict):
    data: List[TwitterData]
    metadata: List[TwitterMetadata]
    aggs: List[TwitterAggs]

