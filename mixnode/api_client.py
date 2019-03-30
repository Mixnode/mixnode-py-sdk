# Standard python packages
import requests
from requests.auth import HTTPBasicAuth   


# Internal imports
from .error import (MixnodeError, KnownMixnodeError, ResponseError, MissingQuery)

class Mixnode(object):

    def __init__(self, api_key=None):
        
        endpoint = 'api.mixnode.com'    

        self._endpoint_url = 'https://' + endpoint

        self.credentials = {
          'api_key': api_key + ':'
        };

        self.isDebugMode = False
        self.response = []

    def _buildRequestParams(self, path, http_method, form_params=None, skip_build_url=False):
        requestParams = {}
        contentTypes = ['application/json']
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
        return self._endpoint_url + path

    def setDebug(self, isDebug):
        self.isDebugMode = isDebug

    def execute(self, query, input_limit=None):
        inputLimit=None
        if (query is None):
          raise MissingQuery()
          
        form_params = {
          'query_str': query
        };

        if (input_limit or input_limit == 0):
          form_params['input_limit'] = input_limit

        return self._execute('/queries', 'POST', form_params)

    def _execute(self, path, http_method, form_params):

        request_params = self._buildRequestParams(path, http_method, form_params) 

        response = self._request(request_params)
        return response

    def _buildrecords(self, raw_response):
        records = []
        if (raw_response.get('rows')):
          for row in raw_response['rows']:
              record = {}
              for index, column in enumerate(raw_response['columns']):
                record[column['name']] = row[index]
              records.append(record)    
        return records 


    def _request(self, request_params):

        fragment = self.__request(request_params)
        if (fragment.get('query_id') and fragment['query_id']):
          self.query_id = fragment['query_id']
          queryPath = '/queries/' + fragment['query_id'] + '/results/1'
          requestParams = self._buildRequestParams(queryPath, 'GET')
          return self._request(requestParams)

        if (fragment.get('next_page') and fragment['next_page']):
            requestParams = self._buildRequestParams(fragment['next_page'], 'GET', None, True)
            return self._request(requestParams)
        return self.response

    def __request(self, request_params):
        try:
            response = requests.request(request_params['method'], request_params['uri'], data=request_params['form'], auth=HTTPBasicAuth(self.credentials['api_key'],''))
            if response.status_code >= 400:
                 raise ResponseError(response)
            
            payload = response.json()    
            self.response = self.response + self._buildrecords(payload)
            return payload
        except MixnodeError as err:
            raise err
     