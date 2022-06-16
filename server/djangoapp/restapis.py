import requests
import json
import logging
# import related models here
from .models import CarDealer
from requests.auth import HTTPBasicAuth
# from ibm_watson import NaturalLanguageUnderstandingV1
#from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
#from ibm_watson.natural_language_understanding_V_1 \
     #import Features, SentimentOptions


# `get_request` to make HTTP GET requests
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
# Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# `post_request` to make HTTP POST requests
def post_request(url, payload, **kwargs):
    print(url)
    print(payload)
    print(kwargs)
    try:
        response = requests.post(url, params=kwargs, json=payload)
    except Exception as e:
        print("Error" ,e)
    print("Status Code ", {response.status_code})
    data = json.loads(response.text)
    return data


# get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
     results = []
    # Call get_request with a URL parameter
     json_result = get_request(url)
     if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result['entries']
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            # Create a CarDealer object with values in `doc` object
            dealer_obj = models.CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)
            print('-------------------------------------------------------')
        return results

# get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_by_id_from_cf(url, dealerId):
    results = []
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        reviews = json_result['entries']
        for review in reviews:
            try:
                review_obj = models.DealerReview(name = review["name"], 
                dealership = review["dealership"], review = review["review"], purchase=review["purchase"],
                purchase_date = review["purchase_date"], car_make = review['car_make'],
                car_model = review['car_model'], car_year= review['car_year'], sentiment= "none")
            except:
                review_obj = models.DealerReview(name = review["name"], 
                dealership = review["dealership"], review = review["review"], purchase=review["purchase"],
                purchase_date = 'none', car_make = 'none',
                car_model = 'none', car_year= 'none', sentiment= "none")
                
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            print(review_obj.sentiment)
                    
            results.append(review_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
     api_key = "uXjcBha35MGEJLotBIaK5ii950K2EBSbOvNtwxjgbbPo"
     url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/f13f64ab-07f4-41e3-8365-d9384a1b6f2a"
     texttoanalyze= text
     version = '2022-03-21'
     authenticator = IAMAuthenticator(api_key)
     natural_language_understanding = NaturalLanguageUnderstandingV1(
     version='2022-03-21',
     authenticator=authenticator
     )
     natural_language_understanding.set_service_url(url)
     response = natural_language_understanding.analyze(
        text=text,
        features= Features(sentiment= SentimentOptions())
# - Get the returned sentiment label such as Positive or Negative
# - Call get_request() with specified arguments
     ).get_request()
     print(json.dumps(response))
     sentiment_score = str(response["sentiment"]["document"]["score"])
     sentiment_label = response["sentiment"]["document"]["label"]
     print(sentiment_score)
     print(sentiment_label)
     sentimentresult = sentiment_label
    
     return sentimentresult





