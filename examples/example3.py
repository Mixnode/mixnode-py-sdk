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


from mixnode import Mixnode
from mixnode.error import MixnodeError
import config 

try:
	client = Mixnode(config.MIXNODE_CONFIG['api_key'])
	# Get 10 higher education market websites that uses wordpress
	query = "SELECT url_host from homepages  where content like '%name=\"generator\" content=\"WordPress%' and url_etld = 'edu' LIMIT 10"
	client.setDebug(True)
	response = client.execute(query)
	print(response)

except MixnodeError as err:
    print(err)
