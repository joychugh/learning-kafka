__author__ = 'jchugh'
import uritools
import base64
import hmac
from hashlib import sha1
import urlparse

def rfc3986_encode(input_string):
    """
    Encodes the input string according to RFC3986 standards
    :param input_string: string to encode
    :type input_string: str
    :return: encoded string
    :rtype: str
    """
    if not isinstance(input_string, str):
        raise TypeError("Expecting string argument")
    if not input_string:
        return ''
    return uritools.uriencode(input_string)

def rfc3986_decode(input_string):
    """
    decodes the RFC3986 encoded input string according to RFC3986 standards
    :param input_string: string to decode
    :type input_string: str
    :return: decoded string
    :rtype: str
    """
    if not isinstance(input_string, str):
        raise TypeError("Expecting string argument")
    if not input_string:
        return ''
    return uritools.uridecode(input_string)

def rfc3986_url_encode(data):
    """
    Takes a dict and url encodes it using rfc3986 standard
    :param data: dictionary of data to be url encoded
    :type data: dict
    :return: urlencoded string
    :rtype: str
    """
    if not data:
        return ''
    sorted_params = sorted(data.items())
    encoded_sorted_data = ['{0}={1}'.format(rfc3986_encode(param[0]), rfc3986_encode(param[1]))
                           for param in sorted_params if len(param) == 2 and param[0] is not None]
    return '&'.join(encoded_sorted_data)

def base64_encode(input_val):
    """
    :param input_val: bytes to be base64 encoded
    :type input_val: buffer or str
    :return:
    """
    return base64.b64encode(input_val)

def get_hmac_sha1_digest(signing_key, message):
    return hmac.HMAC(signing_key, message, sha1).digest()

def rfc3986_url_decode(url):
    return urlparse.parse_qs(rfc3986_decode(url))
