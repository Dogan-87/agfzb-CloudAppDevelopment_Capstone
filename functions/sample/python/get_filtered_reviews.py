# To get filtered reviews 

from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests

secret={
    "COUCH_URL": "https://45c14cd9-04bc-467b-a5fc-65c842636775-bluemix.cloudantnosqldb.appdomain.cloud",
    "IAM_API_KEY": "-lTAU8tc-",
    "COUCH_USERNAME": "45c14cd9-04bc-467b-a5fc-65c842636775-bluemix"
}

def main(dict):
    
    client = Cloudant.iam(
        account_name=secret["COUCH_USERNAME"],
        api_key=secret["IAM_API_KEY"],
        connect=True,
        )  
        
    my_database = client["reviews"]


    try:

        if(dict["id"]):
            selector = {'id': {'$eq': int(dict["id"])}}
            result_by_filter = my_database.get_query_result(selector,raw_result=True)
            result= {
                'headers':{'Content-Type':'application/json'},
                'body':{'data':result_by_filter}

            }
            return result

        if(dict["dealership"]):
            selector = {'dealership': {'$eq': int(dict["dealership"])}}
            result_by_filter = my_database.get_query_result(selector,raw_result=True)
            result= {
                'headers':{'Content-Type':'application/json'},
                'body':{'data':result_by_filter}

            }
            return result

    except:
        print("111111111111111111")
        return {
                'statusCode': 404,
                'message':"Something went wrong"
            }


#reviews_by_id= main({"id":"3"})
#print(reviews_by_id)
reviews_by_dealership= main({"dealership":"46"})
print(reviews_by_dealership)