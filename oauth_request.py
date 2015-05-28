__author__ = 'jchugh'
from oauth_token import Token

"""
A class representing a request
"""

class Request(object):
    def __init__(self, url, method, token=None, query_params=None, payload=None, headers=None, is_streaming=False):
        """
        Initialize the request object
        :param url: target url
        :type url: str
        :param method: the method used to execute the request (GET, POST, PUT, DELETE)
        :type method: str
        :param token: oAuth access token object to be used with this request
        :type token: Token
        :param query_params: query parameters for the request as a dictionary
        :type query_params: dict
        :param payload: request body, as a dictionary
        :type payload: dict
        :param headers: additional headers as a dictionary to send as the part of the request.
        :type headers: dict
        :param is_streaming: boolean value that determines is this request a streaming request.
        :type is_streaming: bool
        :return: the request object
        :rtype: Request
        """
        self.__url = url
        self.__method = method.upper()
        self.__query_params = query_params
        self.__headers = headers
        self.__payload = payload
        self.__is_streaming = is_streaming
        self.__token = token

    def get_url(self):
        return self.__url

    def get_method(self):
        return self.__method

    def get_query_params(self):
        return self.__query_params

    def get_headers(self):
        return self.__headers

    def get_payload(self):
        return self.__payload

    def get_token(self):
        """
        Return the token associated with this request
        :return: token
        :rtype: Token
        """
        return self.__token

    def is_streaming(self):
        """
        Is the request a streaming request?
        :return: boolean to identify if the request is a streaming request
        :rtype: bool
        """
        return self.__is_streaming

    def update_request_payload(self, payload):
        """
        Add to the request payload
        :param payload: A dictionary of additional payload needed
        :type payload: dict
        :return: the updated playload
        :rtype: dict
        """
        if not self.__payload:
            self.__payload = {}
        if not payload:
            return self.__payload
        self.__payload.update(payload)
        return self.__payload

    def update_headers(self, headers):
        """
        Update the headers of the request with a dictionary of headers
        :param headers: Dictionary of headers to update the request headers
        :type headers: dict
        :return: The updated headers
        :rtype: dict
        """
        if not self.__headers:
            self.__headers = {}
        if not headers:
            return self.__headers
        self.__headers.update(headers)
        return self.__headers
