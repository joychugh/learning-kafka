__author__ = 'jchugh'

from simple_oauth.oauth_request import Request

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
        Returns decoded json as a dict
        :return: the tweet as dict
        :rtype: dict
        """
        raw_text = next(self.__data_stream)
        if len(raw_text) > 0:
            try:
                message = self.__json_parser.loads(raw_text)
                if 'text' in message and 'user' in message:
                    return message
            except ValueError as ve:
                return None
        else:
            return None

