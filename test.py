import os
import tweepy
import json
from datetime import datetime

def get_tweets(user):
    client = tweepy.Client(os.getenv('x_bearer_token'))
    try:
        user = client.get_user(username=user)
        user_data = user.data

        tweets = client.get_users_tweets(id=user_data.id, max_results=10)
        tweet_list = [tweet.text for tweet in tweets.data]
        
        result = {
            'user_data': str(user_data),
            'tweets': tweet_list,
            'timestamp': datetime.now().isoformat()
        }
        
        # 使用时间戳创建文件名
        filename = f'{datetime.now().strftime("%Y_%m%d_%H%M%S")}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
            
        return result

    except tweepy.TweepyException as e:
        error_result = {
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }
        filename = f'twitter_log_{datetime.now().strftime("%Y_%m%d_%H%M%S")}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(error_result, f, ensure_ascii=False, indent=2)
        return error_result

if __name__ == "__main__":
    print(get_tweets('ilyasut'))