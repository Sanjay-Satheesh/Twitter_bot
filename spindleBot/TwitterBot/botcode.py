import tweepy
import logging
from config import create_api
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def check_mentions(api, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        
        logger.info(f"Answering to {tweet.user.name}")
        statusa = api.get_status(tweet.id, tweet_mode = "extended")
        full_text = statusa.full_text
        print("The text of the status is : \n\n" + full_text)
        

        if tweet.in_reply_to_status_id is not None:
            
            parent_tweet=api.get_status(tweet.in_reply_to_status_id)
            statusb = api.get_status(parent_tweet.id, tweet_mode = "extended")
            replytwt = statusb.full_text
            print(parent_tweet.user.screen_name+": "+replytwt)
        else:
            replytwt = "."            
           
        cont = full_text + "Rply: " + replytwt
        msg = "DM:"
        api.send_direct_message(tweet.user.id, msg)
        api.send_direct_message(tweet.user.id, cont)
         
        
    return new_since_id

def main():
    api = create_api()
    since_id = 1
    while True:
        since_id = check_mentions(api, since_id)
        logger.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()