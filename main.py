__author__ = 'jchugh'
from kafka import KafkaClient
from oauth import Oauth
from oauth_request import Request
from oauth_token import Token
import ConfigParser
from ConfigParser import NoOptionError
from twitter import TwitterStream

try:
    import simplejson as json
except ImportError:
    import json


CONFIG = ConfigParser.ConfigParser()
CONFIG.read("configurations.ini")

KAFKA = KafkaClient('{host}:{port}'.format(
    host=CONFIG.get('kafka', 'host'),
    port=CONFIG.get('kafka', 'port')
    )
)

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

twitter = TwitterStream(oauth_client)
data_stream = twitter.get_stream(request)


def start_streaming(stream):
    raw_text = next(stream)
    try:
        item = json.loads(raw_text)
        if 'text' in item:
            print item['text']
    except json.scanner.JSONDecodeError as e:
        pass

max_stream = int(CONFIG.get('twitter', 'max_stream_responses'))
if max_stream < 0:
    while True:
        start_streaming(data_stream)
else:
    for i in range(0, max_stream):
        start_streaming(data_stream)