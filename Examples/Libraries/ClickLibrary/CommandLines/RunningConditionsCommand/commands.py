import click
from CommandLines import cli

@click.command()
@click.argument('crawler_name', required=False)
def running_condition_option(crawler_name):
    """
    CRAWLER_NAME is name of crawler
    """
    print('this')
    print(crawler_name)

# @click.command()
# def crawler_option(crawler_name: str):
#     '''cralwer options are reddit_crawler and twitter_crawler'''
#     click.echo(f'you select crawler_option = {crawler_name}')
#
# @click.command()
# def collection_name(selected_collection_name: str):
#     '''
#     collection_name depends on crawler class you selected
#     for RedditCrawler, options are general, country, region, states_subreddit, work_from_home, lockdown, social_distance
#     for TwitterCrawler, options are twitter_tweet and twitter_geo
#     '''
#     click.echo(f'you selected collection_name = {selected_collection_name}')
#
# @click.command()
# def respond_type(respond_type_name: str):
#     click.echo(f"you selected respond_type = {respond_type_name}")
#
# @click.command()
# def search_type(search_type_name: str):
#     click.echo(f"you selected search_type = {search_type_name}")
#
# @click.command()
# def sort(sort_name: str):
#     """sort have the following option asc or desc"""
#     click.echo(f"you selected sort = {sort_name}")
#
# @click.command()
# def verbose(verbose_boolean: bool):
#     click.echo(f"you selected verbose = %s" %(verbose_boolean and 'True' or 'False'))
