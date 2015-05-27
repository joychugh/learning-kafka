__author__ = 'jchugh'
import uuid
import time
import oauth_utils
import requests
import copy
from oauth_request import Request
from oauth_token import Token

"""
A library to help with oAuth1 requests
"""

class Oauth(object):
    """
    oAuth1 provides easy to use encapsulation around oAuth requests.
    Currently only support HMAC-SHA1 signatures.
    """
    def __init__(self, consumer_key,
                 consumer_secret,
                 request_token_url,
                 access_token_url,
                 authorize_url,
                 invalidate_token_url,
                 version='1.0',
                 token=None):
        self.__consumer_key = consumer_key
        self.__signature_method = 'HMAC-SHA1'
        self.__version = version
        self.__consumer_secret = consumer_secret
        self.__signing_key = None
        self.__signature_base_string = None
        self.__parameter_string = None
        self.__auth_headers = None
        self.__token = token
        self.__signature = None
        self.__authorization_header_value = None
        self.__access_token_url = access_token_url
        self.__request_token_url = request_token_url
        self.__authorize_url = authorize_url
        self.__invalidate_token_url = invalidate_token_url
        self.__response = None
        self.__request = None

    def __initialize_authorization_headers(self):
        auth_headers = {'oauth_consumer_key': self.__consumer_key,
                        'oauth_nonce': Oauth._get_nonce(),
                        'oauth_signature_method': self.__signature_method,
                        'oauth_timestamp': Oauth._get_timestamp(),
                        'oauth_version': self.__version,
                        'oauth_callback': 'oob'}
        if self.__token:
            auth_headers['oauth_token'] = self.__token.get_token()
        self.__auth_headers = auth_headers

    def __generate_parameter_string(self):
        parameter_string_payload = self.__auth_headers
        if self.__request.get_payload():
            parameter_string_payload.update(self.__request.get_payload())
        if self.__request.get_query_params():
            parameter_string_payload.update(self.__request.get_query_params())
        self.__parameter_string = oauth_utils.rfc3986_url_encode(parameter_string_payload)

    def __generate_signature_base_string(self):
        self.__signature_base_string = '{method}&{request_url}&{parameter_string}'.format(
            method=oauth_utils.rfc3986_encode(self.__request.get_method()),
            request_url=oauth_utils.rfc3986_encode(self.__request.get_url()),
            parameter_string=oauth_utils.rfc3986_encode(self.__parameter_string))

    def __generate_signing_key(self):
        encoded_consumer_secret = oauth_utils.rfc3986_encode(self.__consumer_secret)
        encoded_token_secret = ''
        if self.__token:
            encoded_token_secret = oauth_utils.rfc3986_encode(self.__token.get_secret())
        self.__signing_key = '{consumer_secret}&{token_secret}'.format(
            consumer_secret=encoded_consumer_secret,
            token_secret=encoded_token_secret)

    def __generate_signature_hmac_sha1(self):
        hmac_sha1_digest = oauth_utils.get_hmac_sha1_digest(self.__signing_key, self.__signature_base_string)
        self.__signature = oauth_utils.base64_encode(hmac_sha1_digest)

    def __update_authorization_headers_with_signature(self):
        self.__auth_headers['oauth_signature'] = self.__signature

    def __generate_authorization_header_value(self):
        authorization_header = 'OAuth ' + ','.join(map(lambda t: '{0}="{1}"'.format(oauth_utils.rfc3986_encode(t[0]),
                                                                                    oauth_utils.rfc3986_encode(t[1])),
                                                       sorted(self.__auth_headers.items())))
        self.__request.update_headers({'Authorization': authorization_header})

    def get_content(self):
        """
        Returns the content of the response
        :return: the response content
        :rtype: str
        """
        return self.__response.content

    def get_status_code(self):
        """
        Returns the response status code
        :return: request status code
        :rtype: int
        """
        return self.__response.status_code

    def get_response(self):
        """
        Returns the full response object, in most cases this would not be necessary.
        :return: the response object
        :rtype: requests.models.Response
        """
        return self.__response

    def make_request(self, request, token=None):
        """
        Initiate the request
        :param request: The request to initiate
        :type request: Request
        :return: None
        :rtype: None
        """
        self.__request = request
        self.__token = token
        if not self.__token:
            original_request = copy.deepcopy(self.__request)
            self.__get_auth_token_and_secret()
            self.__request = original_request
        self.__prepare_request()
        self.__make_request(self.__request)

    def invalidate_token(self, token):
        """
        Invalidate the given token
        :param token: The token to invalidate
        :type token: Token
        :return: The invalidated token value
        :rtype: dict
        """
        self.__token = token
        self.__request = Request(self.__invalidate_token_url, 'POST', payload={'access_token': token.get_token()})
        self.__prepare_request()
        self.__make_request(self.__request)
        if self.get_status_code() == '200':
            return self.get_response()

    def get_token(self):
        return self.__token

    def generate_token(self):
        """
        Generate the token and return it
        :return: generated access token
        :rtype: Token
        """
        self.__get_auth_token_and_secret()
        return self.get_token()

    def __prepare_request(self):
        self.__initialize_authorization_headers()
        self.__generate_parameter_string()
        self.__generate_signature_base_string()
        self.__generate_signing_key()
        self.__generate_signature_hmac_sha1()
        self.__update_authorization_headers_with_signature()
        self.__generate_authorization_header_value()

    def __get_auth_token_and_secret(self):
        # Step 1 Get Request Tokens and Secret
        self.__request = Request(self.__request_token_url, 'POST')
        self.__prepare_request()
        self.__make_request(self.__request)
        self.__set_oauth_token_and_secret(self.get_content())

        # Step 2 get Access Tokens
        self.__request = Request(self.__access_token_url, 'POST')
        print "Visit {authorize_url}?oauth_token={request_token} " \
              "on your browser authorize the app and enter the pin".format(authorize_url=self.__authorize_url,
                                                                           request_token=self.__token.get_token())
        oauth_verifier = raw_input("Enter the pin you got from the browser: ")
        self.__request = Request(self.__access_token_url, 'POST', payload={'oauth_verifier': oauth_verifier})
        self.__prepare_request()
        self.__make_request(self.__request)
        self.__set_oauth_token_and_secret(self.get_content())

    def __set_oauth_token_and_secret(self, api_response):
        oauth_request_tokens = oauth_utils.rfc3986_url_decode(api_response)
        oauth_token = str(oauth_request_tokens['oauth_token'][0])
        oauth_token_secret = str(oauth_request_tokens['oauth_token_secret'][0])
        self.__token = Token(oauth_token, oauth_token_secret)

    def __make_request(self, request):
        """
        Make the request
        :param request: the request object
        :type request: Request
        :return: None
        :rtype: None
        """
        method = request.get_method()
        if method == 'POST':
            self.__response = requests.post(request.get_url(),
                                            data=oauth_utils.rfc3986_url_encode(request.get_payload()),
                                            json=None,
                                            params=oauth_utils.rfc3986_url_encode(request.get_query_params()),
                                            headers=request.get_headers())
        elif method == 'GET':
            self.__response = requests.get(request.get_headers(),
                                           params=oauth_utils.rfc3986_url_encode(request.get_query_params()),
                                           headers=request.get_headers())
        elif method == 'PUT':
            self.__response = requests.put(request.get_url(),
                                           data=oauth_utils.rfc3986_url_encode(request.get_payload()),
                                           params=oauth_utils.rfc3986_url_encode(request.get_query_params()),
                                           headers=request.get_headers())
        elif method == 'DELETE':
            self.__response = requests.delete(request.get_url(),
                                              params=oauth_utils.rfc3986_url_encode(request.get_query_params()),
                                              headers=request.get_headers())
        else:
            raise TypeError("Invalid or unsupported request method")

    @staticmethod
    def _get_nonce():
        """
        Returns a fairly random nonce. Since the number of requests wont be really high being used
        for streaming, this should work.
        :return: nonce
        :rtype: str
        """
        return uuid.uuid4().get_hex()

    @staticmethod
    def _get_timestamp():
        """
        Returns the UNIX timestamp from system clock as a string.
        :return: UNIX timestamp as a string
        :rtype: str
        """
        return str(int(time.time()))
