import requests

class Crawler(object):
    def __init__(self):
        pass

    def prepare_crawler(self):
        pass

    def apply_crawling_strategy(self):
        pass

    def get_response(self):
        pass

    def make_request(self):
        pass

    def run(self):
        """
        run function does all of the request qhich may or may not
        required more than 1 make_request call
        """
    def run_once(self):
        pass


class RedditCrawler(Crawler):

    def __init__(self, how_data_is_collected):

        super(RedditCrawler, self).__init__()
        self.prepare_crawler(how_data_is_collected)

    def prepare_crawler(self, how_data_is_collected):
        self.current_condition = None

    def apply_crawling_strategy(self, res_content):
        pass

    def get_response(self, request_url):
        res_content = requests.get(request_url)
        return res_content

    def make_request(self):
        pass

    def run(self):
        while True:
            res_content =self.run_once()
            saved_file = get_saved_file_path()
            save_to_file(res_content, saved_file)  # utility function
        return res_content

    def run_once(self):
        request_url = self.make_request()
        res_content = self.get_response(request_url)
        res_content = self.apply_crawling_strategy(res_content)
        return res_content

def select_crawler_condition(crawler_type, how_data_is_collected):
    """given param=how_data_is_collected, crawler_option is chosen"""
    if crawler_type == 'reddit':
        crawler = RedditCrawler(how_data_is_collected)
    else:
        raise  ValueError('')
    return crawler


def check_running_condition(running_condition):
    pass



# def run_crawler_once(selected_crawler):
#
#     res_content = selected_crawler.run()
#     saved_file = get_saved_file_path()
#     save_to_file(res_content, saved_file)  # utility function

def get_crawler(crawler_option):
    SelectedCrawler = RedditCrawler
    return SelectedCrawler


def run_crawler(crawler_option):
    SelectedCrawler = get_crawler(crawler_option)

    while True:
        selected_crawler = SelectedCrawler()
        res_content = selected_crawler.run()
        # run_crawler_once(selected_crawler)


def main():
    running_conditions = None
    check_running_condition(running_condition)
    crawler_condition = select_crawler_condition(crawler_type='reddit', how_data_is_collected='avg')
    run_crawler(crawler_condition)

def save_to_file(param, param1):
    pass

def get_saved_file_path():
    pass

if __name__ == '__main__':
    main()

