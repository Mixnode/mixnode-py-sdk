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


# Standard python packages
import requests
from requests.auth import HTTPBasicAuth   


# Internal imports
from .error import (MixnodeError, ResponseError, MissingQuery, MissingApiKey)

class Mixnode(object):
    """
    Constructs a :class:`Mixnode <Mixnode>`.

    Examples:
        client = Mixnode('Your_API_KEY')

    :param api_key: API Key obtained from Mixnode Portal.
    :return: :class:`Mixnode <Mixnode>` object
    """
    def __init__(self, api_key=None):
        
        self._endpoint_url = 'https://api.mixnode.com'
        if (api_key is None):
          raise MissingApiKey()
        self.credentials = {
          'api_key': api_key + ':'
        };
        self.isDebugMode = False
        self.response = []

    def _buildRequestParams(self, path, http_method, form_params=None, skip_build_url=False):
        """
        Constructs request parameters.

        :param path: query path which will be used in the URI.
        :param http_method:
        :param form_params:
        :param skip_build_url:
        :return: : request parameters which will be needed for firing query
        """
        requestParams = {}
        if (skip_build_url):
            requestParams['uri'] = path
        else:    
            requestParams['uri'] = self._buildUrl(path)
        requestParams['method'] = http_method
        headers = {}
        requestParams['form'] = form_params
        requestParams['headers'] = headers
        if self.isDebugMode:
            print ('request parameters were')
            print ('request method: ' + requestParams['method'])
            print ('request uri: ' + requestParams['uri'])
            if (http_method == 'POST'):
                print (requestParams['form'])
        return requestParams

    def _buildUrl(self, path):
        """
        Concatenates end point with the path

        :param path: query path which will be used in the URI.
        """
        return self._endpoint_url + path

    def setDebug(self, isDebug):
        """
        Enables debugging and logs the queries being sent to Mixnode Server

        :param path: isDebug <boolean>
        """
        self.isDebugMode = isDebug

    def execute(self, query, input_limit=None):
        """
        Interface exposing functionality to make calls to Mixnode server

        :param query:  SQL query sent to the backend
        :param input_limit:  Sets the input limit on the data to be scanned
        """

        if (query is None):
          raise MissingQuery()
          
        form_params = {
          'query_str': query
        };

        if (input_limit or input_limit == 0):
          form_params['input_limit'] = input_limit

        return self._execute('/queries', 'POST', form_params)

    def _execute(self, path, http_method, form_params):
        """
        Private function to implement execute workflow

        :param path: URL to invoke.
        :param http_method:  HTTP method to use 
        :param form_params:  A map of form parameters and their values.
        """
        request_params = self._buildRequestParams(path, http_method, form_params) 
        response = self._request(request_params)
        return response

    def _buildrecords(self, raw_response):
        """
         Builds Mixnode raw response to array of objects where objects are based 
         on columns of the tables requested via query

        :param raw_response:  raw response returned by Mixnode SQL engine
        """
        records = []
        if (raw_response.get('rows')):
          for row in raw_response['rows']:
              record = {}
              for index, column in enumerate(raw_response['columns']):
                record[column['name']] = row[index]
              records.append(record)    
        return records 


    def _request(self, request_params):
        """
        Function to handle as below:
        1. timeout if supplied by the user wants to cancel the query after certain period of time
        2. handles paging response from Mixnode server.
        Find more about it here https://www.mixnode.com/docs/sql-api/queries

        :param request_params:  request parameters which will be needed for firing subsequent queries
        """

        # Fires first POST request with parameters
        fragment = self.__request(request_params)
        if (fragment.get('query_id') and fragment['query_id']):
          self.query_id = fragment['query_id']
          # Once we have the query id, fire page 1 GET request
          queryPath = '/queries/' + fragment['query_id'] + '/results/1'
          requestParams = self._buildRequestParams(queryPath, 'GET')
          return self._request(requestParams)
        # Subsequent requests should have next_page attribute along with the paging
        # information to make subsequent calls.
        if (fragment.get('next_page') and fragment['next_page']):
            requestParams = self._buildRequestParams(fragment['next_page'], 'GET', None, True)
            return self._request(requestParams)
        # Returns the built response once the next_page attribute is not a part of response from previous requests
        return self.response

    def __request(self, request_params):
        """
        Synchronous function to make API calls using requests library

        :param request_params:  request parameters which will be needed for firing subsequent queries
        """
        try:
            response = requests.request(request_params['method'], request_params['uri'], data=request_params['form'], auth=HTTPBasicAuth(self.credentials['api_key'],''))
            if response.status_code >= 400:
                 raise ResponseError(response)
            payload = response.json()    
            self.response = self.response + self._buildrecords(payload)
            return payload
        except MixnodeError as err:
            raise err
     