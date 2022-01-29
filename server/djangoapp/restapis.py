import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        if "api_key" in kwargs:
            response = requests.get(url, headers={'Content-Type':'application/json'}, params=kwargs, auth=HTTPBasicAuth("apikey", api_key))
        else:
            response = requests.get(url, headers={'Content-Type':'application/json'}, params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, payload, **kwargs):
    print(url)
    #payload["review"]["id"]=1120
    print(payload)
    print(kwargs)
    json_obj = payload["review"]
    print(json_obj)
    try:
        response = requests.post(url, params=kwargs, json=payload)
        print(response)
    except Exception as e:
        print("Error" ,e)
    print("Status Code ", {response.status_code})
    data = json.loads(response.text)
    print(data)
    return data  

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["body"]
        print(dealers)
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            #print(dealer)
            dealer_doc = dealer["doc"]
            #dealer_doc = dealer["docs"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer( address=dealer_doc["address"],
                                    city=dealer_doc["city"], 
                                    full_name=dealer_doc["full_name"],
                                    id=dealer_doc["id"],
                                    lat=dealer_doc["lat"],
                                    long=dealer_doc["long"],
                                    short_name=dealer_doc["short_name"],
                                    st=dealer_doc["st"],
                                    zip=dealer_doc["zip"])
            results.append(dealer_obj)
            print(dealer_obj)
            print('Dealer object appended')
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_by_id_from_cf(url, dealer_id):
    results = []
    json_result = get_request(url, dealerId=dealer_id)
    if json_result:
        reviews = json_result['docs']
        print(dealer_id)
        print(reviews)
        a=[]
        for review in reviews:
            a.append(review["dealership"])
        print(a)
        for review in reviews:
            #change review["id"] to review["dealership"]
            if (dealer_id in a) and (review["dealership"]==dealer_id):
                try:
                    review_obj = DealerReview(
                        name = review["name"], 
                        dealership = review["dealership"], 
                        review = review["review"], 
                        purchase=review["purchase"],
                        purchase_date = review["purchase_date"], 
                        car_make = review['car_make'],
                        car_model = review['car_model'], 
                        car_year= review['car_year'], 
                        sentiment= "none",
                        id = review["id"])
                except:
                    review_obj = DealerReview(
                        name = review["name"], 
                        dealership = review["dealership"], 
                        review = review["review"], 
                        purchase=review["purchase"],
                        purchase_date = 'none', 
                        car_make = 'none',
                        car_model = 'none', 
                        car_year= 'none', 
                        sentiment= "none",
                        id = review["id"])
                    
                review_obj.sentiment = analyze_review_sentiments(review_obj.review)
                print(review_obj.sentiment) 
                results.append(review_obj)
        
                
    print(results)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview, **kwargs):
    API_KEY="s-M4PU0F56QH7IoKmgZ9CrvOA1mvMkAMpaL9cnmTsZuA"
    NLU_URL='https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/e9d88f37-5d4b-4fae-b418-99e857e27c5f/v1/analyze?version=2020-08-01'
    text_to_analyze= dealerreview
    version = '2020-08-01'
    authenticator = IAMAuthenticator(API_KEY)
    
    natural_language_understanding = NaturalLanguageUnderstandingV1(version=version,authenticator=authenticator)
    natural_language_understanding.set_service_url(NLU_URL)
    try:
        response = natural_language_understanding.analyze(
            text=text_to_analyze,
            features= Features(sentiment= SentimentOptions())
        ).get_result()
        
        print(json.dumps(response))
        sentiment_score = str(response["sentiment"]["document"]["score"])
        sentiment_label = response["sentiment"]["document"]["label"]
        print(sentiment_score)
        print(sentiment_label)
        sentimentresult = sentiment_label
    except:
        sentimentresult = "neutral"

    return sentimentresult


