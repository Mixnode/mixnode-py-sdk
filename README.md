# Mixnode Python SDK 


## Overview
The Mixnode [Python](https://www.python.org/) SDK allows you to easily integrate the Mixnode REST APIs into your Python application.

### Requirements
* Python2 and above.
* A Mixnode API key from a registered user on the [Mixnode portal](https://www.mixnode.com/account/api).


### Installation
```sh
pip install mixnode-python-sdk
```

## Tutorial
Follow this tutorial to see a step-by-step guide and examples of how to use the Mixnode Python SDK.

### Get the API key from Mixnode portal
* Create an account on [Mixnode](https://www.mixnode.com/signup).
* If already registered, then login and navigate to api key page. 
* Dashboard -> Choose API from left menu -> Note the API key. 
* Or, directly navigate to https://www.mixnode.com/account/api to find your API key.

### Authentication
This SDK comes with basic authentication over HTTPS which requires you to pass your Mixnode API key using a config file or as a string during client instantiation. 

#### Basic Authentication

This type of token is given directly to the application.

``` Python
import Mixnode

# Create an instance of the Mixnode Client
client = Mixnode("Your API Key") #add your API KEY here; available at https://www.mixnode.com/account/api

```
Note that `api_key` can also be passed as a JSON object in a config file to avoid specifying the key in the code.
Please see [Examples](https://github.com/Mixnode/mixnode-py-sdk/blob/master/examples)

#### Quick Start

```Python

from mixnode import Mixnode

client = Mixnode("Your api key")
query = "SELECT url, title from homepages LIMIT 10"
response = client.execute(query)

```

#### Mixnode's execute functionality
`execute` is a synchronous operation which builds response based on paging Mixnode SQL API. 

##### execute can accept upto two parameters : query, inputLimit (optional). 
Please see various [Examples](https://github.com/Mixnode/mixnode-py-sdk/blob/master/examples) for usage details.
```Python
try:
 response = Mixnode("Your API Key").execute(query)
 # Do something with response
except MixnodeError as error:
 # Do something with error
```
```Python
try:
 # Fires a query and also sets the input limit on the data to be scanned
 response = Mixnode("Your API Key").execute(query, inputLimit)
 # Do something with response
except MixnodeError as error:
 # Do something with error
```

#### SDK debugging
* Turning on the debug mode logs the HTTP requests being sent to the Mixnode API.
* This is useful to verify if the queries being sent are correct.
* This is useful to verify if the execution is in progress.

```Python
# Setting debug to true logs the state of the application.
# Do not use this in production.
Mixnode("Your API Key").setDebug(True);

```

## Examples: Mixnode Python Client
[Examples](https://github.com/Mixnode/mixnode-py-sdk/tree/master/examples)

## SQL API Documentation

You can get the full documentation for the API on the [Mixnode SQL API reference](https://www.mixnode.com/docs/sql-api/introduction)


## Support

[hi@mixnode.com](mailto:hi@mixnode.com)
