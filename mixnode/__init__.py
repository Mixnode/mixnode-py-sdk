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


"""
mixnode - Mixnode Python SDK
~~~~~~~~~~~~~~~~~~~~~

   >>> import mixnode
   >>> client = Mixnode('Your API Key')

:license: Apache 2.0, see LICENSE for more details.
"""

__title__ = 'mixnode-py-sdk'
__author__ = 'Mixnode'
__version__ = '1.0.0'
__license__ = 'Apache 2.0'

from .api_client import Mixnode
from .error import (MixnodeError, KnownMixnodeError, ResponseError, ResponseServerError)
