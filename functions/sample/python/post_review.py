from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests 

secret={
    "COUCH_URL": "https://45c14cd9-04bc-467b-a5fc-65c842636775-bluemix.cloudantnosqldb.appdomain.cloud",
    "IAM_API_KEY": "-lTAU8tc-rHV1d0JQqwjHTyD7SYClm4nPLWPG7yML22F",
    "COUCH_USERNAME": "45c14cd9-04bc-467b-a5fc-65c842636775-bluemix"
}

def main(dict):

    try:
        
        client = Cloudant.iam(
        account_name=secret["COUCH_USERNAME"],
        api_key=secret["IAM_API_KEY"],
        connect=True,
        ) 
        
        my_database = client["reviews"]
        
        selector = {'id': {'$exists': True}}
        result_by_filter = my_database.get_query_result(selector,raw_result=True)
        res = [ sub['id'] for sub in result_by_filter["docs"] ]
        
        if dict["review"]["id"] not in res:
            new_document = my_database.create_document(dict["review"])
    
        if(new_document.exists()):
            result= {
            'headers':{'Content-Type':'application/json'},
            'body':{'data':"Data posted"}
            }
    except:
        
        return {
        'statusCode': 404,
        'message': "Error in Post"
        }  
        
    return result

dict={ "review": 
    { "id": 1114, "name": "Upkar Lidder", "dealership": 15,
    "review": "Great service!","purchase": "false", "another": "field",
    "purchase_date": "02/16/2021","car_make": "Audi", "car_model": "Car",
    "car_year": 2021 } }

posted_review = main(dict)
print(posted_review)


















"""from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests 

secret={
    "COUCH_URL": "https://45c14cd9-04bc-467b-a5fc-65c842636775-bluemix.cloudantnosqldb.appdomain.cloud",
    "IAM_API_KEY": "-lTAU8tc-rHV1d0JQqwjHTyD7SYClm4nPLWPG7yML22F",
    "COUCH_USERNAME": "45c14cd9-04bc-467b-a5fc-65c842636775-bluemix"
}




client = Cloudant.iam(
        account_name=secret["COUCH_USERNAME"],
        api_key=secret["IAM_API_KEY"],
        connect=True,
        ) 

def post_request(url, json_payload, **kwargs):

    json_data = json.dumps(json_payload, indent=4)
    print(f"{json_data}")

    try:
        # Call get method of requests library with URL and parameters
        response = requests.post(url, params=kwargs, json=json_data)

    except Exception as e:
        # If any error occurs
        print("Network exception occurred")
        print(f"Exception: {e}")

    print(f"With status {response.status_code}")
    print(f"Response: {response.text}")

a= post_request("https://45c14cd9-04bc-467b-a5fc-65c842636775-bluemix.cloudantnosqldb.appdomain.cloud",
{ "review": { "id": 1114, "name": "Upkar Lidder", "dealership": 15,
 "review": "Great service!", "purchase": "false", "another": "field",
  "purchase_date": "02/16/2021", "car_make": "Audi", "car_model": "Car",
   "car_year": 2021 } }
)
print(a)"""