import os
import tweepy


# print(os.getenv('x_bearer_token'))
client = tweepy.Client(os.getenv('x_bearer_token'))

try:
    user = client.get_user(username="elonmusk")
    user_data = user.data
    print(user_data)

    tweets = client.get_users_tweets(id=user_data.id, max_results=10)
    for tweet in tweets.data:
        print(f"推文: {tweet.text}")

except tweepy.TweepyException as e:
    print(f"错误: {e}")