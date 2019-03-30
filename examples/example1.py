from mixnode import Mixnode
from mixnode.error import MixnodeError
import config 

client = Mixnode(config.MIXNODE_CONFIG['api_key'])

try:
    query = "SELECT url, title from pages where url_domain = 'cnn.com' LIMIT 10"
    client.setDebug(True)
    response = client.execute(query)
    print(response)

except MixnodeError as err:
    print(err)
