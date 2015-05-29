__author__ = 'jchugh'

from oauth import Oauth
from oauth_request import Request

class TwitterStream(object):
    """
    A class representing twitter client to get streaming tweets
    """
    def __init__(self, oauth, json_parser):
        """
        Initialize the twitter streaming client with the Oauth instance
        :param Oauth: Oauth instance configured for twitter.
        :type Oauth: Oauth
        :return: `TwitterStream` instance
        """
        self.__oauth = oauth
        self.__json_parser = json_parser
        self.__response_stream = None

    def get_tweets(self, request):
        """
        Get the tweets from the given request
        :param request: the streaming request
        :type request: Request
        :return: `Tweets` instance
        :rtype: Tweets
        """
        self.__oauth.make_request(request)
        self.__response_stream = self.__oauth.get_response_content_iterator()
        return Tweets(self.__response_stream, self.__json_parser)

class Tweet(object):
    """
    Class representing a tweet
    """
    def __init__(self, message, user_id):
        """
        Tweet
        :param message: the tweet
        :type message: str
        :param user_id: the user id who sent this tweet
        :type user_id: str
        :return: the tweet
        :rtype: Tweet
        """
        self.__message = message
        self.__user_id = user_id

    def get_message(self):
        return self.__message

    def get_user_id(self):
        return self.__user_id

class Tweets(object):

    def __init__(self, data_stream, json_parser):
        """
        Initialize the `Tweets` class
        :param data_stream: raw data stream iterator from Twitter
        :type data_stream: iterator
        :param json_parser: json parser to parse the json data
        :type json_parser: `Json`
        :return: `Tweets` object
        :rtype: Tweets
        """
        self.__data_stream = data_stream
        self.__json_parser = json_parser

    def __iter__(self):
        return self

    def next(self):
        """
        Returns a tuple of Tweet,UserID
        :return: tuple of tweet and userid who made the tweet
        :rtype: Tweet
        """
        raw_text = next(self.__data_stream)
        if len(raw_text) > 0:
            try:
                message = self.__json_parser.loads(raw_text)
                if 'text' in message and 'user' in message:
                    return Tweet(message['text'].encode('utf-8'), message['user']['id_str'].encode('utf-8'))
            except ValueError as ve:
                return None
        else:
            return None

