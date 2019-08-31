# import tweepy

# # Authenticate to Twitter
# auth = tweepy.OAuthHandler("pvXFqDgkwb1bzFFvINvhHlKbk", "sVW9ES5mVqTz6jd9JKBPML1vcxdoryLj2ecSz2hwZVRt4caSds")
# auth.set_access_token("1167785350040887296-tlExXqQJO7aEr0PvHhdAmceWQSO5sj", "uZ6r7KZaCSE6bpEjkQyQnWTQz6p2m9LmGU5B1lgo5bOnb")
# api = tweepy.API(auth)
# try:
#     api.verify_credentials()
#     print("Authentication OK")
# except:
#     print("Error during authentication")
# # Create API object


# # Create a tweet
# api.update_status("Hello Tweepy")

import json
import tweepy

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        print(f"{tweet.user.name}:{tweet.text}")

    def on_error(self, status):
        print("Error detected")

# Authenticate to Twitter
auth = tweepy.OAuthHandler("pvXFqDgkwb1bzFFvINvhHlKbk", "sVW9ES5mVqTz6jd9JKBPML1vcxdoryLj2ecSz2hwZVRt4caSds")
auth.set_access_token("1167785350040887296-tlExXqQJO7aEr0PvHhdAmceWQSO5s", "uZ6r7KZaCSE6bpEjkQyQnWTQz6p2m9LmGU5B1lgo5bOnb")

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)

api.mentions_timeline()

tweets_listener = MyStreamListener(api)
stream = tweepy.Stream(api.auth, tweets_listener)
stream.filter(track=["Python", "Django", "Tweepy"], languages=["en"])