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
from nose.tools import raises, assert_is_not_none
from unittest import TestCase

from mixnode import Mixnode
from mixnode.error import ResponseError, MixnodeError

from tests.assets import MixnodeData
from tests.fixtures import ApiClientJsonData

def mocked_requests_post(*args, **kwargs):
    endpoint_url = 'https://api.mixnode.com'
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    query_id = ApiClientJsonData.data['dummyQueryObject']['query_id']
    if args[1] == endpoint_url + '/queries':
        return MockResponse(ApiClientJsonData.data['dummyQueryObject'], 200)
    elif args[1] == endpoint_url + '/queries/'+ query_id + '/results/1':
        return MockResponse(ApiClientJsonData.data['dummyPage1Response'], 200)
    elif args[1] == endpoint_url + '/queries/'+ query_id + '/results/2':
        return MockResponse(ApiClientJsonData.data['dummyPage2Response'], 200)

    return MockResponse(None, 404)

class ExecuteTest(TestCase):
    @mock.patch('mixnode.api_client.requests.request', side_effect=mocked_requests_post)
    def execute_should_provide_response(self, mock_get):
        query = "SELECT * from homepages LIMIT 5"
        client = Mixnode('XXXXX')
        client.setDebug(True)
        response = client.execute(query)
        assert_is_not_none(response)
