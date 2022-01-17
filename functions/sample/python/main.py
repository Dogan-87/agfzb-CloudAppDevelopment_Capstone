#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
# To return NAMES of ALL DATABASEs 
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests

secret={
    "COUCH_URL": "Your URL", 
    "IAM_API_KEY": "Your API KEY", 
    "COUCH_USERNAME": "Your Username" 
}

def main(dict):
    databaseName = "dealerships"
    

    try:
        client = Cloudant.iam(
            account_name=secret["COUCH_USERNAME"],
            api_key=secret["IAM_API_KEY"],
            connect=True,
        )
        print("Databases: {0}".format(client.all_dbs()))

    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"dbs": client.all_dbs()}
