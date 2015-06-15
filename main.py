__author__ = 'jchugh'
from multiprocessing import Process
from ConfigParser import NoOptionError
from simple_kafka import kafka_client
from simple_oauth.oauth import Oauth
from simple_oauth.oauth_request import Request
from simple_oauth.oauth_token import Token
from twitter import TwitterStream
from config import config
from kafka import KeyedProducer
from simple_spark_example import spark_example

try:
    import simplejson as json
except ImportError:
    import json


try:
    token = Token(config.get('oauth', 'access_token'),
                  config.get('oauth', 'access_token_secret'))
except NoOptionError as e:
    # No token, get it from twitter and make the request
    # In this case, watch for the console output to visit the given URL to authorize the app and enter the PIN
    token = None


def send_messages(t_tweets, k_producer, k_topic, skip_invalid=False, max_skip=0):
    tweet = next(t_tweets)
    skips = 0
    while skip_invalid and not tweet and skips < max_skip:
        tweet = next(t_tweets)
        skips += 1
    if tweet is None:
        return
    try:
        k_producer.send(topic=k_topic,
                        key=tweet['user']['id_str'],
                        msg=tweet['text'].encode('utf-8'))
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



def init():
    oauth_client = Oauth(config.get('oauth', 'consumer_key'),
                         config.get('oauth', 'consumer_secret'),
                         config.get('oauth', 'request_token_url'),
                         config.get('oauth', 'access_token_url'),
                         config.get('oauth', 'authorize_url'),
                         version=config.get('oauth', 'version'))

    request = Request(url=config.get('twitter', 'streaming_filter_url'),
                      method="POST",
                      is_streaming=True,
                      headers={'Accept-Encoding': 'deflate, gzip '},
                      payload={'locations': '-118.39,30.41,-59.61,49.46'},
                      token=token)

    max_stream = int(config.get('twitter', 'max_stream_responses'))
    topic = config.get('kafka', 'topic')
    max_skip_invalid_responses = config.getint('twitter', 'max_skip_invalid_response')
    skip_invalid_responses = config.getboolean('twitter', 'skip_invalid')
    producer = KeyedProducer(kafka_client, async=True)

    twitter = TwitterStream(oauth_client, json)
    tweets = twitter.get_tweets(request)

    # Starts here.
    try:
        if max_stream < 0:
            send_unlimited_messages(tweets, producer, topic)
        else:
            send_limited_messages(max_stream,
                                  tweets,
                                  producer,
                                  topic,
                                  skip_invalid_responses,
                                  max_skip_invalid_responses)
    except Exception as e:
        print e
    finally:
        producer.stop()
        kafka_client.close()

if __name__ == '__main__':
    p = Process(target=init)
    p.start()
    spark_example.start_spark()

    # If limited stream to get, wait till we get the given number of streams.
    # If unlimited, terminate the process
    if config.get('twitter', 'max_stream_responses') > 0:
        p.join()
    else:
        p.terminate()


