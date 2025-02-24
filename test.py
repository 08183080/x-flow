import os
import tweepy
import json
import time
import yagmail
import schedule
from datetime import datetime

def get_contents(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def get_emails(path):
    with open(path, 'r') as f:
        return f.read().splitlines()

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
        filename = './twitter_data/' + f'{datetime.now().strftime("%Y_%m%d_%H_%M_%S")}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
            
        return result

    except tweepy.TweepyException as e:
        error_result = {
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }
        filename = './twitter_data/' + f'{datetime.now().strftime("%Y_%m%d_%H_%M_%S")}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(error_result, f, ensure_ascii=False, indent=2)
        return error_result


def send_email(src, dst, subject, contents):
    pwd = os.environ.get('wangyi_emai_auth')

    yag = yagmail.SMTP(user=src, password=pwd, host='smtp.163.com', port='465')
    yag.send(to=dst, subject=subject, contents=contents)
    yag.close()

def send_emails(src, tos, subject, contents):
    for to in tos:
        send_email(src, to, subject, contents)  


def daily_task():
    try:
        src = '19121220286@163.com'
        tos = get_emails('emails.txt') 
        subject = '今日AI+头条项目'
        contents = get_tweets('elonmusk')
        print(contents)
        send_emails(src, tos, subject, contents)
    except Exception as e:
        print(f"{e} occured in daily_task")

if __name__ == "__main__":
    # print(get_tweets('elonmusk'))
    try:
        schedule.every().day.at('00:10').do(daily_task)

        while True:
            schedule.run_pending()
            time.sleep(1)

    except Exception as e:
        print(f"{e} occured~")