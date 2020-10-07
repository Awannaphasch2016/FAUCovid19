# -*- coding: utf-8 -*-

"""Declare all types that will be used in different modules."""
import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from typing_extensions import Literal
from typing_extensions import TypedDict

# RunningConditions = Dict[str, str]

Url = str
RedditAggs = Dict
TwitterAggs = Dict

Json = Dict[str, Any]
# Tags = Optional[Union[List[str], str, List[None]]]
Tags = Union[List[str], str]
Query = Optional[List[str]]
Crawler_type = str

# res = {'a': 1}
# r = json.dumps(res)
# y = json.loads(r)
# Json = type(y)

# Frequency = Literal["day"]
Frequency = Literal["day", "hour", "minute", "second"]
Sort = Literal["asc", "desc"]
epoch_datetime = int


class TwitterCollectionkey(TypedDict):
    """Skipped."""

    aspect: Tags
    query: Query


class TwitterCollection(TypedDict):
    """Skipped."""

    collection: TwitterCollectionkey
    name: str


class SubredditCollectionKey(TypedDict):
    """Skipped."""

    subreddit: List[str]
    query: Query
    aspect: Any  # VALIDATE: what is the type of aspect?


class SubredditCollection(TypedDict):
    """Skipped."""

    collection: SubredditCollectionKey
    name: str


class RedditRunningConstraints(TypedDict):
    """Skipped."""

    aggs: Optional[str]
    after: int
    before: Optional[int]
    size: int
    metadata: str
    sort: Sort
    fields: Optional[str]


class TwitterRunningConstraints(TypedDict):
    """Skipped."""

    aggs: Optional[str]
    after: int
    before: Optional[int]
    size: Optional[int]  # None = all
    metadata: str
    sort: Sort
    fields: Optional[Union[str, List[str]]]  # None = all


class RunningConditions(TypedDict):
    """Skipped."""

    crawler_option: str
    collection_name: str
    respond_type: str
    search_type: str
    sort: Sort
    # tag: Optional[str]
    tag: Tags
    max_after: int


RunningConditionsKeyValue = List[
    Tuple[
        List[Union[str, None, int]],
        RunningConditions,
    ],
]


class RedditMetadata(TypedDict, total=False):
    """Skipped."""

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
    aspect: Tags
    query: Query


class TwitterMetadata(TypedDict):
    """Skipped."""

    running_constraints: TwitterRunningConstraints
    # after: str  # VALIDATE: is after str or int?
    after: int  # VALIDATE: is after str or int?
    aggs: Any  # VALIDATE: what is the correct type?
    before: Optional[int]
    execution_time_milliseconds: float
    frequency: Frequency
    results_returned: Optional[int]  # VALIDATE: what is the correct type?
    size: int
    sort: Sort
    timed_out: Optional[bool]  # VALIDATE: what is the correct type?
    # search_words: List[str]
    search_words: TwitterCollectionkey  # VALIDATE: what is the correct type?
    total_results: int
    fields: List[str]
    aspect: Tags
    query: Query
    index: Any


class RedditData(TypedDict):
    """Skipped."""

    # common_fields
    author: str
    author_flair_richtext: Optional[str]
    author_flair_type: Optional["str"]
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
    """Skipped."""

    author_fullname: str  # to author_fullname
    to: Optional[str]
    body: str  # body
    retweets: int
    favorites: int  # to score
    replies: int
    id: str
    premalink: str
    author_id: int
    created_utc: epoch_datetime  # to craeted_ utc
    formatted_date: str
    hashtags: str
    mentions: str
    geo: str
    full_link: Url  # to full_linh
    retrieved_on: epoch_datetime
    date: Union[datetime.datetime, epoch_datetime]

    # Added later
    sentiment_polarity: float


class RedditResponse(TypedDict):
    """Skipped."""

    data: List[RedditData]
    # metadata: List[RedditMetadata]
    metadata: RedditMetadata  # VALIDATE: what is the correct type?
    aggs: List[RedditAggs]


class TwitterResponse(TypedDict):
    """Skipped."""

    data: List[TwitterData]
    metadata: List[TwitterMetadata]
    aggs: List[TwitterAggs]
