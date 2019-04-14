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


import pytest
import mock
from nose.tools import raises, assert_is_not_none, assert_equal
from unittest import TestCase

from mixnode import Mixnode
from mixnode.error import ResponseError, MixnodeError

from tests.assets import MixnodeData
from tests.fixtures import ApiClientJsonData

endpointUrl = 'https://api.mixnode.com'
query = "SELECT * from homepages LIMIT 5"

def mocked_requests(*args, **kwargs):    
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    query_id = ApiClientJsonData.data['dummyQueryObject']['query_id']
    if args[1] == endpointUrl + '/queries':
        return MockResponse(ApiClientJsonData.data['dummyQueryObject'], 200)
    elif args[1] == endpointUrl + '/queries/'+ query_id + '/results/1':
        return MockResponse(ApiClientJsonData.data['dummyPage1Response'], 200)
    elif args[1] == endpointUrl + '/queries/'+ query_id + '/results/2':
        return MockResponse(ApiClientJsonData.data['dummyPage2Response'], 200)
    return MockResponse(None, 404)

def mocked_requests_server_error(*args, **kwargs):    
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    query_id = ApiClientJsonData.data['dummyQueryObject']['query_id']
    if args[1] == endpointUrl + '/queries':
        return MockResponse(ApiClientJsonData.data['dummyQueryObject'], 200)
    elif args[1] == endpointUrl + '/queries/'+ query_id + '/results/1':
        return MockResponse(ApiClientJsonData.data['dummyPage1Response'], 200)
    elif args[1] == endpointUrl + '/queries/'+ query_id + '/results/2':
        return MockResponse(ApiClientJsonData.data['dummyServerErrorResponse'], 200)
    return MockResponse(None, 404)

class ExecuteTest(TestCase):
    def setUp(self):
        self.client = Mixnode('XXXXX')
        self.client.setLag(0) # This is to speed up the test and not wait between subsequent requests

    def tearDown(self):
        self.client = None

    def test_api_client_base_path(self):
        assert_equal(self.client.endpointUrl, endpointUrl)

    @raises(MixnodeError)
    def test_api_client_missing_query_error(self):
        response = self.client.execute()

    def test_api_client_execute_is_defined(self):
        assert_is_not_none(self.client.execute)

    def test_api_client_debug(self):
        assert_equal(self.client.isDebugMode, False)
        self.client.setDebug(True)
        assert_equal(self.client.isDebugMode, True)

    def test_buildRequestParams_1(self):
        path = '/path'
        http_method = 'POST'
        form_params = {'key1': 'value1'}
        requestParams = self.client._buildRequestParams(path, http_method, form_params)
        assert_equal(requestParams['uri'], endpointUrl+path)
        assert_equal(requestParams['method'], http_method)
        assert_equal(requestParams['form'], form_params)
        assert_equal(requestParams['headers'], {})

    def test_buildUrl(self):
        path = '/path'
        full_path = self.client._buildUrl(path)
        assert_equal(endpointUrl + path, full_path)

    def test_buildrecords(self):
        raw_response = {
            "columns": [{
                "name": 'col1'
                }
            ],
            "rows": [['val1'], ['val2']]
          }
        records = self.client._buildrecords(raw_response)
        assert_equal(records[0]['col1'], "val1")
        assert_equal(records[1]['col1'], "val2")

    @mock.patch('mixnode.api_client.requests.request', side_effect=mocked_requests)
    def test_execute_should_provide_response(self, mock_get):
        query = "SELECT * from homepages LIMIT 5"
        response = self.client.execute(query)
        assert_equal(response[0]['url'], ApiClientJsonData.data['dummyPage2Response']['rows'][0][0])
        assert_equal(response[1]['url'], ApiClientJsonData.data['dummyPage2Response']['rows'][1][0])
    
    @mock.patch('mixnode.api_client.requests.request', side_effect=mocked_requests_server_error)
    @raises(MixnodeError)
    def test_response_server_error(self, mock_get):
        self.client.execute(query)

class ExecuteTestWithoutSetup(TestCase):
    @raises(MixnodeError)
    def test_api_client_no_api_key_error(self):
        self.client = Mixnode()     