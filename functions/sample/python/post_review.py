from cloudant.client import Cloudant
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
print(a)