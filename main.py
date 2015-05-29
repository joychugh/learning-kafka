__author__ = 'jchugh'
from kafka import KafkaClient
from oauth import Oauth
from oauth_request import Request
from oauth_token import Token
import ConfigParser
from ConfigParser import NoOptionError
from twitter import TwitterStream, Tweets
from kafka import KeyedProducer
try:
    import simplejson as json
except ImportError:
    import json


CONFIG = ConfigParser.ConfigParser()
CONFIG.read("configurations.ini")

try:
    token = Token(CONFIG.get('oauth', 'access_token'),
                  CONFIG.get('oauth', 'access_token_secret'))
except NoOptionError as e:
    # No token, get it from twitter and make the request
    # In this case, watch for the console output to visit the given URL to authorize the app and enter the PIN
    token = None

oauth_client = Oauth(CONFIG.get('oauth', 'consumer_key'),
                     CONFIG.get('oauth', 'consumer_secret'),
                     CONFIG.get('oauth', 'request_token_url'),
                     CONFIG.get('oauth', 'access_token_url'),
                     CONFIG.get('oauth', 'authorize_url'),
                     version=CONFIG.get('oauth', 'version'))

request = Request(url=CONFIG.get('twitter', 'streaming_sample_url'),
                  method="POST",
                  is_streaming=True,
                  headers={'Accept-Encoding': 'deflate, gzip '},
                  token=token)

kafka_client = KafkaClient(CONFIG.get('kafka', 'hosts'))
producer = KeyedProducer(kafka_client, async=True)
twitter = TwitterStream(oauth_client, json)
max_stream = int(CONFIG.get('twitter', 'max_stream_responses'))
tweets = twitter.get_tweets(request)
topic = CONFIG.get('kafka', 'topic')
max_skip_invalid_responses = CONFIG.get('twitter', 'max_skip_invalid_response')
skip_invalid_responses = CONFIG.get('twitter', 'skip_invalid')


def send_messages(t_tweets, k_producer, k_topic, skip_invalid=False, max_skip=0):
    tweet = next(t_tweets)
    skips = max_skip
    while skip_invalid and not tweet and skips < max_skip:
        tweet = next(t_tweets)
        skips += 1
    if tweet is None:
        return
    try:
        k_producer.send(topic=k_topic,
                        key=tweet.get_user_id(),
                        msg=tweet.get_message())
    except Exception as ex:
        print "-------"
        print "Error with sending message"
        print str(ex)
        print "-------"


def send_unlimited_messages(t_tweets, k_producer, k_topic):
    while True:
        send_messages(t_tweets, k_producer, k_topic)

def send_limited_messages(count, d_stream, t_tweets, k_topic, skip_invalid, max_skip):
    for i in range(0, count):
        send_messages(d_stream, t_tweets, k_topic, skip_invalid, max_skip)

# Starts here.
try:
    if max_stream < 0:
        send_unlimited_messages(tweets, producer, topic)
    else:
        send_limited_messages(max_stream, tweets, producer, topic, skip_invalid_responses, max_skip_invalid_responses)
except Exception as e:
    print e
finally:
    producer.stop()
    kafka_client.close()



def print_response(response):
    if response:
        print(response[0].error)
        print(response[0].offset)

