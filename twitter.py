__author__ = 'jchugh'

from oauth import Oauth
from oauth_request import Request

class TwitterStream(object):
    """
    A class representing twitter client to get streaming tweets
    """
    def __init__(self, oauth):
        """
        Initialize the twitter streaming client with the Oauth instance
        :param Oauth: Oauth instance configured for twitter.
        :type Oauth: Oauth
        :return: `TwitterStream` instance
        """
        self.__oauth = oauth

    def get_stream(self, request):
        """
        Get the stream iterator from the given request
        :param request: the streaming request
        :type request: Request
        :return: streaming data iterator
        :rtype: iterator
        """
        self.__oauth.make_request(request)
        return self.__oauth.get_response_content_iterator()




