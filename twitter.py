__author__ = 'jchugh'
from main import CONFIG
import oauth
from oauth_request import Request
from oauth_token import Token

oauth_ins = oauth.Oauth(CONFIG.get('oauth', 'consumer_key'),
                        CONFIG.get('oauth', 'consumer_secret'),
                        CONFIG.get('oauth', 'request_token_url'),
                        CONFIG.get('oauth', 'access_token_url'),
                        CONFIG.get('oauth', 'authorize_url'),
                        CONFIG.get('oauth', 'access_token_url'),
                        version=CONFIG.get('oauth', 'version'))

## TODO this class has a lot of work to do.