class MixnodeError(Exception):
    """
    Base class for all exceptions

    :param message: User defined message.
    """
    def __init__(self, message, **kwargs):
        super(MixnodeError, self).__init__(**kwargs)
        self.message = message

    def __str__(self):
        return "{name}: message: {message}".format(
            name=self.__class__.__name__,
            message=self.message
        )

class ResponseError(MixnodeError):
    def __init__(self, response):
        super(ResponseError, self).__init__(message='')
        raw_response = response.json()
        self.status_code = response.status_code
        self.message = raw_response['errors']['message']

# Common error responses listed here

class KnownMixnodeError(MixnodeError):
    def __init__(self, **kwargs):
        super(KnownMixnodeError, self).__init__(message=self.message, **kwargs)

class RequestTimeout(KnownMixnodeError):
    message = 'Request timed out before getting a response'

class Network(KnownMixnodeError):
    message = 'Network issue, see err.more for details'

class MissingApiKey(KnownMixnodeError):
    message = 'Missing api_key definition in the configuration while instantiating Mixnode Client'

class MissingConfiguration(KnownMixnodeError):
    message = 'Missing configuration while instantiating Mixnode Client'

class MissingQuery(KnownMixnodeError):
    message = 'Missing the required parameter (query) on calling execute'

class QueryTimeout(KnownMixnodeError):
    message = 'Query was cancelled due to user defined timeout'

class Unknown(KnownMixnodeError):
    message = 'Unknown error occured'

KNOWN_ERRORS = {
    'RequestTimeout': RequestTimeout,
    'Network': Network,
    'MissingApiKey': MissingApiKey,
    'MissingConfiguration': MissingConfiguration,
    'MissingQuery': MissingQuery,
    'QueryTimeout': QueryTimeout,
    'Unknown': Unknown
}
