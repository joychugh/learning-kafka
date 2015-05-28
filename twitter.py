__author__ = 'jchugh'
from main import CONFIG
import oauth
from oauth_request import Request
from oauth_token import Token
from ConfigParser import NoOptionError

try:
    import simplejson as json
except ImportError:
    import json

oauth_client = oauth.Oauth(CONFIG.get('oauth', 'consumer_key'),
                           CONFIG.get('oauth', 'consumer_secret'),
                           CONFIG.get('oauth', 'request_token_url'),
                           CONFIG.get('oauth', 'access_token_url'),
                           CONFIG.get('oauth', 'authorize_url'),
                           version=CONFIG.get('oauth', 'version'))


request = Request("https://stream.twitter.com/1.1/statuses/sample.json", "POST",
                  is_streaming=True,
                  headers={'Accept-Encoding': 'deflate, gzip '})

try:
    token = Token(CONFIG.get('oauth', 'access_token'),
                  CONFIG.get('oauth', 'access_token_secret'))
    response = oauth_client.make_request(request, token)
except NoOptionError as e:
    # No token, get it from twitter and make the request
    # In this case, watch for the console output to visit the given URL to authorize the app and enter the PIN
    response = oauth_client.make_request(request)

def start_streaming(stream):
    raw_text = next(stream)
    try:
        item = json.loads(raw_text)
        if 'text' in item:
            print item['text']
    except json.scanner.JSONDecodeError as e:
        pass


data_stream = response.iter_lines()
max_stream = int(CONFIG.get('twitter', 'max_stream_responses'))
if max_stream < 0:
    while True:
        start_streaming(data_stream)
else:
    for i in range(0, max_stream):
        start_streaming(data_stream)

