__author__ = 'jchugh'

class Token(object):
    """
    A class representing a token
    """
    def __init__(self, token, secret):
        """
        Get an instance of Token
        :param token: the oauth token value
        :type token: str
        :param secret: the oauth token secret
        :type secret: str
        :return: the Token instance
        :rtype: Token
        """
        if not token or not secret:
            raise TypeError("Token class both the token value and the secret")
        self.__token = token
        self.__secret = secret

    def get_token(self):
        return self.__token

    def get_secret(self):
        return self.__secret
