import os
from c8 import C8Client

C8_APIKEY = os.getenv("C8_APIKEY")
C8_EMAIL = os.getenv("C8_EMAIL")
C8_PASSWORD = os.getenv("C8_PASSWORD")

C8_CONNECTION = { 'protocol' :'https',
                    'host' : 'gdn.paas.macrometa.io', 
                    'port' : 443, 
                    'geofabric' : '_system',
                    'email' : C8_EMAIL,
                    'password' : C8_PASSWORD
}

client = C8Client(**C8_CONNECTION)
print(client)


collection_name = "cxResults"

if not client.has_collection(collection_name):
    client.create_collection(collection_name)

collection = client.get_collection(collection_name)

value = "INSERT { \
        'firstname':@firstname, \
        'lastname':@lastname, \
        'email':@email, \
        'zipcode':@zipcode, \
        '_key': 'abc'} \
        IN %s" % collection_name

parameter = {"firstname": "", "lastname": "", "email": "", "zipcode": ""}

insert_data = {"query": {"name": "insertRecord", "parameter": parameter, "value": value}} 
