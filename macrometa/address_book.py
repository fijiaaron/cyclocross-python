import os
from c8 import C8Client

C8_APIKEY = os.getenv("C8_APIKEY")xXXXXXX
C8_EMAIL = os.getenv("C8_EMAIL")
C8_PASSWORD = os.getenv("C8_PASSWORD")

C8_CONNECTION = { 'protocol' :'https',
                    'host' : 'gdn.paas.macrometa.io', 
                    'port' : 443, 
                    'geofabric' : '_system',
                    'email' : C8_EMAIL,
                    'password' : C8_PASSWORD
}


collection_name = "employees"

value = "INSERT {'firstname':@firstname, 'lastname':@lastname, 'email':@email, 'zipcode':@zipcode, '_key': 'abc'} IN %s" % collection_name
parameter = {"firstname": "", "lastname": "", "email": "", "zipcode": ""}

insert_data = {"query": {"name": "insertRecord", "parameter": parameter, "value": value}} 
get_data = {"query": {"name": "getRecords", "value": "FOR doc IN %s RETURN doc" % collection_name}}
update_data = {"query": {"name": "updateRecord", "value": "UPDATE 'abc' WITH { \"lastname\": \"cena\" } IN %s" % collection_name }}
delete_data= {"query": {"name": "deleteRecord", "value": "REMOVE 'abc' IN %s" % collection_name}}
get_count = {"query": {"name": "countRecords", "value": "RETURN COUNT(FOR doc IN %s RETURN 1)" % collection_name}}



if __name__ == "__main__":

    print("\n ------- CREATE GEO-REPLICATED COLLECTION  ------")
    if client.has_collection(collection_name):
      print("Collection exists")
    else:
      employees = client.create_collection(collection_name)
    print("Created collection: {}".format(collection_name))

print("\n ------- CREATE GEO-REPLICATED COLLECTION  ------")
if client.has_collection(collection_name):
    print("Collection exists")
else:
    employees = client.create_collection(collection_name)
print("Created collection: {}".format(collection_name))


print("\n ------- CREATE RESTQLs  ------")
client.create_restql(insert_data)  # name: insertRecord
client.create_restql(get_data)  # name: getRecords
client.create_restql(update_data)  # name: updateRecord
client.create_restql(delete_data)  # name: deleteRecord
client.create_restql(get_count)  # name: countRecords
print("Created RESTQLs:{}".format(client.get_restqls()))