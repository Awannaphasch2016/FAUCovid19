# TODO: figure out a way to use sqlite to regroup all data into each
#   aspect. what is the sqlite cmd for this?
import sqlite3
from typing import Any
from typing import Dict
from typing import List

from global_parameters import ALL_ASPECTS
from global_parameters import ALL_CRAWLERS
from src.Sources.Preparations.Data import get_keywords_collections
from src.Sources.Preparations.Data.social_media_crawler import \
    _get_crawler_tags_words

dbfile: str = \
    'C:/Users/Anak/PycharmProjects/Covid19CookieCutter/Data/Processed/' \
    'reddit_database.db'

(
    General,
    Country,
    Region,
    states_subreddit,
    social_distance_keywords,
    lockdown_keywords,
    work_from_home_keywords,
    covid_keywords,
    reopen_keywords,
) = get_keywords_collections(ALL_CRAWLERS[1])

# =====================
# == group data by aspect
# =====================
conn = sqlite3.connect(dbfile)


def execute_sqlite_query(aspect_name: str) -> List[Dict[str, Any]]:
    def get_subreddit_for_aspect(aspect_name: str) -> List[str]:
        return General + Country + Region + states_subreddit

    def get_keyword_for_aspect(aspect_name: str) -> List[str]:
        # VALIDATE: haven't test below paragraph
        tag_words = _get_crawler_tags_words(
            crawler=ALL_CRAWLERS[1],
            tag=aspect_name,
            work_from_home_keywords=work_from_home_keywords,
            lockdown_keywords=lockdown_keywords,
            social_distance_keywords=social_distance_keywords,
            corona_keywords=covid_keywords,
            reopen_keywords=reopen_keywords,
        )
        return tag_words

    def get_all_data_for_aspect(
            crawler_name: str,
            aspect_subreddits: List[str],
            aspect_keywords: List[str],
    ) -> List[str]:

        aspect_database_name: str
        if crawler_name == 'reddit':
            aspect_database_name = 'reddit_stream'
        else:
            raise ValueError

        all_aspect_subreddit_query = \
            list(
                map(
                lambda x: "'" + x + "'",
                aspect_subreddits,
                )
            )
        all_aspect_subreddit_query_str = ','.join(all_aspect_subreddit_query)

        aspect_keywords_query: List[str] = \
            list(map(
                lambda x: "body LIKE '%" + x + "%'",
                [i for i in aspect_keywords])
            )
        aspect_keywords_query_str: str = ' OR '.join(aspect_keywords_query)

        aspect_query = f"""
            select *
            from {aspect_database_name}
            where subreddit in ({all_aspect_subreddit_query_str}) AND  
            ({aspect_keywords_query_str})
            ;
            """

        def execute_sqlite_query(aspect_query: str) -> Any:
            c = conn.cursor()
            c.execute(aspect_query)
            query_result =  c.fetchall()

            table_scheama =  c.execute("PRAGMA table_info("
                                       "'reddit_stream')").fetchall()

            return query_result

        query_result: Any = execute_sqlite_query(aspect_query)

        return query_result

    aspect_subreddits: List[str] = get_subreddit_for_aspect(aspect_name)
    aspect_keywords: List[str] = get_keyword_for_aspect(aspect_name)
    all_aspect_data: List[str] = \
        get_all_data_for_aspect(
            ALL_CRAWLERS[1],
            aspect_subreddits,
            aspect_keywords,
        )

    return all_aspect_data

aspect_name = ALL_ASPECTS[2]
execute_sqlite_query(aspect_name)

conn.commit()
conn.close()

# NOTE: I uncommented below paragraph
# rf_top = rand_func(49,55)
# svm_top = rand_func(43,52)
# lr_top  = rand_func(47,55)
# mlp_top = rand_func(43,52)
#
# no_strategy = [rf_top, svm_top, lr_top, mlp_top]
#
#
# rf_top_strategy  = rand_func(50,60)
# svm_top_strategy = rand_func(48,60)
# lr_top_strategy  = rand_func(49,55)
# mlp_top_strategy   = rand_func(59,63)
