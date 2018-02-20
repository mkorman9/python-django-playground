import re
from urllib.parse import urlparse

ALLOWED_URL_PREFIXES = ('http://', 'https://')
DEFAULT_URL_PREFIX = 'http://'
URL_LOCAL_IP_REGEX = re.compile(r'''
(localhost)|(127\.)|(192\.168\.)|(10\.)|(172\.1[6-9]\.)|(172\.2[0-9]\.)|(172\.3[0-1]\.)|(::1$)|([fF][cCdD])
''')


class ModelValidationException(Exception):
    def __init__(self, message):
        self.message = message


class URL(object):
    def __init__(self, address):
        if not address:
            raise ModelValidationException("empty url")
        elif '.' not in address:
            raise ModelValidationException("url must contain at least one dot character")

        address = self._force_protocol_prefix(address)

        parsed_url = urlparse(address)
        if URL_LOCAL_IP_REGEX.findall(parsed_url.netloc):
            raise ModelValidationException("url represents invalid network location")

        self._address = address

    @property
    def address(self):
        return self._address

    def _force_protocol_prefix(self, url):
        url_lower = url.lower()

        for prefix in ALLOWED_URL_PREFIXES:
            if url_lower.startswith(prefix):
                break
        else:
            url = '{}{}'.format(DEFAULT_URL_PREFIX, url)

        return url