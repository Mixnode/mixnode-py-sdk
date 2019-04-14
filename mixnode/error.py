# -*- coding: utf-8 -*-
# Mixnode Python SDK
# Turn the web into a database
# A fast, flexible and massively scalable platform to extract and analyze data from the web.
#
# Contact: hi@mixnode.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class MixnodeError(Exception):
    """
    Base class for all exceptions

    :param message: User defined message.
    """
    def __init__(self, message, status_code=None, status=None, **kwargs):
        super(MixnodeError, self).__init__(**kwargs)
        self.message = message
        self.status_code = status_code
        self.status = status

    def __str__(self):
        return "{name}: status: {status} status_code: {status_code} message: {message} ".format(
            name=self.__class__.__name__,
            message=self.message,
            status_code=self.status_code,
            status = self.status
        )

class ResponseError(MixnodeError):
    """
    ResponseError is raised when an API call doesn't succeed.
    raises :exc:`ResponseError` accordingly.

    :param response: Response from http client :class:`requests.request`.
    """
    def __init__(self, response):
        super(ResponseError, self).__init__(message='', status_code='', status='')
        raw_response = response.json()
        self.status_code = response.status_code
        self.message = raw_response['errors']['message']

class ResponseServerError(MixnodeError):
    """
    ResponseServerError is raised when the query/server have some error o
    as defined in QUERY_ERROR_STATUS below.
    raises :exc:`ResponseServerError` accordingly.

    :param response: Response from http client :class:`requests.request`.
    """
    def __init__(self, response):
        super(ResponseServerError, self).__init__(message='', status_code='', status='')
        self.status = response['status']
        self.message = response['message']

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

QUERY_STATUS = {
  'PLANNING': 'PLANNING',
  'RUNNING': 'RUNNING',
  'FINISHED': 'FINISHED'
}

QUERY_ERROR_STATUS = {
  'USER_CANCELED'
  'FAILED': 'FAILED',
  'SYNTAX_ERROR': 'SYNTAX_ERROR',
  'GENERIC_INTERNAL_ERROR': 'GENERIC_INTERNAL_ERROR',
  'PERMISSION_DENIED': 'PERMISSION_DENIED',
  'OUTPUT_LIMIT_EXCEEDED': 'OUTPUT_LIMIT_EXCEEDED',
  'INSUFFICIENT_RESOURCES': 'INSUFFICIENT_RESOURCES',
  'BLOCKED': 'BLOCKED',
  'USER_ERROR': 'USER_ERROR',
  'EXTERNAL_ERROR': 'EXTERNAL_ERROR',
  'DIVISION_BY_ZERO': 'DIVISION_BY_ZERO',
  'EXCEEDED_MEMORY_LIMIT': 'EXCEEDED_MEMORY_LIMIT',
  'INPUT_LIMIT_EXCEEDED': 'INPUT_LIMIT_EXCEEDED',
  'UNKNOWN_ERROR': 'UNKNOWN_ERROR',
  'FATAL_ERROR': 'FATAL_ERROR'
}

def _buildError(status, error_msg):
    oError = {
        'status': status,
        'message': error_msg
      }
    return oError;

def GetError(status, error_msg):
    hasError = QUERY_ERROR_STATUS.get(status)
    if hasError:
        return _buildError(status, error_msg)
    if (error_msg):
        return _buildError(QUERY_ERROR_STATUS['FATAL_ERROR'], error_msg)    