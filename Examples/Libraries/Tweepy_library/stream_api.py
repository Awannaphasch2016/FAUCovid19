from __future__ import absolute_import, print_function

import time

from tweepy import OAuthHandler, Stream, StreamListener

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key = "M2dcKnRZGqBWTrPBXeefFHHjZ"
consumer_secret = "ktTB1WAJNsZBnKTddPqHMpzczj7ehZigXtN77YIFUdSlZ1EW7v"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token = "1140239819127365632-zgNBmmiLvfUV4ZXywwFMCaltCbOWW0"
access_token_secret = "bD0sjo0Jj2In2KldOw4PhHVhsiVShlQizY5R5l2gn9PMG"


class StdOutListener(StreamListener):
    """A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def __init__(self):
        self.count = 0
        self.s = time.time()

    def on_data(self, data):
        # print(self.count)
        self.f = time.time()
        diff = self.f - self.s
        print(diff)

        if (diff) > 11:
            # count = 4
            # time = 13.340330123901367
            # tweet / sec = 0.29984265478058525
            print(f"count = {self.count}")
            print(f"time = {diff}")
            print(f"tweet/sec = {self.count/diff}")
            exit()

        # print(data)
        self.count += 1
        return True

    def on_error(self, status):
        print(status)


if __name__ == "__main__":
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=["basketball"])
