import logging

# create logger
module_logger = logging.getLogger("spam_application.auxiliary")


class Auxiliary:
    def __init__(self):
        self.logger = logging.getLogger("spam_application.auxiliary.Auxiliary")
        self.logger.info("creating an instance of Auxiliary")

    def do_something(self):
        self.logger.info("doing something")
        a = 1 + 1
        self.logger.info("done doing something")
        self.logger.error("error")
        self.logger.debug("debug")


def some_function():
    module_logger.info(f"received a call to {some_function.__name__}")
