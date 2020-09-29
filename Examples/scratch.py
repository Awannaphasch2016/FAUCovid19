import logging
#
# log = logging.getLogger('hello')
# log.setLevel(logging.DEBUG)
#
# # # Create a file handler to store the logs
# file_handler = logging.FileHandler('test.log')
# log.addHandler(file_handler)
#
# # # Send output to terminal
# stream_handler = logging.StreamHandler()
# log.addHandler(stream_handler)
#
# log.debug('debug log')

# logging.basicConfig()
# log = logging.getLogger('hello')
# log.setLevel(logging.DEBUG)
# print(log.getEffectiveLevel())
# log.debug('debug log')
# log.critical('critical log')

import logging
import sys

# Initialize Logger and set Level to DEBUG
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# logger.setLevel(logging.CRITICAL)

# Initialize a Handler to print to stdout
handler = logging.StreamHandler(sys.stdout)

# Format Handler output
logFormatter = logging.Formatter(
    "%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p"
)
handler.setFormatter(logFormatter)

# Set Handler Level to DEBUG
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)


logger.debug('Debug Info')
logger.info('info Info')
logger.critical('critical Info')
print(logger.level)
# >>> 09/19/2020 09:01:00 PM Debug Info

