import requests
import json
import logging
# import related models here
from .models import CarDealer
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions
import time


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
def get_dealerships_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealership_bystate_from_cf(url, dealerId):
    results = []
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        dealers=json_result['body']
        for review in reviews:
            try:
                review_obj = models.DealerReview(name = review["name"], 
                dealership = review["dealership"], review = review["review"], purchase=review["purchase"],
                purchase_date = review["purchase_date"], car_make = review['car_make'],
                car_model = review['car_model'], car_year= review['car_year'], sentiment= "none"),
                full_name=dealer_doc["full_name"]
            except:
                review_obj = models.DealerReview(name = review["name"], 
                dealership = review["dealership"], review = review["review"], purchase=review["purchase"],
                purchase_date = 'none', car_make = 'none',
                car_model = 'none', car_year= 'none', sentiment= "none"),
                full_name=dealer_doc["full_name"]
                
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            print(review_obj.sentiment)
                    
            results.append(review_obj)

    return results

def get_reviews_from_cf(url, **kwargs):
    results = []
    dealerId = kwargs.get("dealerId")
    json_result = get_request(url, dealerId=dealerId)

    if json_result:
        reviews = json_result["dealerReviews"]

        for review in reviews:
            sentiment = analyze_review_sentiments(review["review"])
            if review["purchase"] is False:
                review_obj = models.DealerReview(
                name = review["name"],
                purchase = review["purchase"],
                dealership = review["dealership"],
                review = review["review"],
                purchase_date = None,
                car_make = "",
                car_model = "",
                car_year = "",
                sentiment = sentiment,
                id = review["id"]
                )
                print(review_obj.sentiment)
                results.append(review_obj)
            else:
                review_obj = models.DealerReview(
                name = review["name"],
                purchase = review["purchase"],
                dealership = review["dealership"],
                review = review["review"],
                purchase_date = review["purchase_date"],
                car_make = review["car_make"],
                car_model = review["car_model"],
                car_year = review["car_year"],
                sentiment = sentiment,
                id = review["id"]
                )
                print(review_obj.sentiment)
            results.append(review_obj)
    return results   

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
     api_key = "kxyznQ9NtkhZQ_Ypz4iJ6OG7DVJzhvJbwFT9sp-PI3hA"
     url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/ec68dcd7-9bef-4e63-a8ac-9dd27c7f5574"
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





