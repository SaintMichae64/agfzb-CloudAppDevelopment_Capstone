from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarMake, CarModel, CarDealer, DealerReview, ReviewPost
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/about.html', context)


# a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == 'GET':                                     
        return render(request, 'djangoapp/contact.html', context)

# a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    url = "https://quincy.mybluemix.net/"
    # dealerships = get_dealers_from_cf(url)
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('/djangoapp/')
        else:
            # If not, return to login page again
            context["message"]="Username or password is incorrect."
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)
# `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('/djangoapp')

# `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        # serializer = 
        return render(request, 'djangoapp/registration.html', context)
        
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST.get('username', False)
        password = request.POST.get('psw', False)
        first_name = request.POST.get('firstname', False)
        last_name = request.POST.get('lastname', False)
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
            # Login the user and redirect
            login(request, user)
            return redirect("/djangoapp/")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://quincy.mybluemix.net/dealerships/dealer-get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        context = {'dealerships' : dealerships}
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)

# `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://quincy.mybluemix.net"
        apikey="86LCWp_sISZS-VSr_bsvzVZ7gvcoWdmqFw1q7JvnpM5H"
        dealer_details = get_dealer_reviews_from_cf(url, dealerId=dealer_id)
        reviewsdict = (vars(review) for review in dealer_details)
        context = {"Reviews":reviewsdict, "dealerId":dealer_id}
        print(reviewsdict)
        return render(request, 'djangoapp/dealer_details.html', context)


# `add_review` view to submit a review
def add_review(request, dealer_id):

    if request.user.is_authenticated:
        context={}
        if request.method == "GET":
            cars = models.CarModel.objects.filter(dealer_id=dealer_id)
            
            context['cars'] = cars
            context['dealer_id']=dealer_id
            return render(request, 'djangoapp/add_review.html', context)
        elif request.method == "POST":
            print(request.POST)
            url = "https://d47998ca.us-south.apigw.appdomain.cloud/api/review"
            review = {}
            
            review["id"] = get_reviews_count(url) + 1
            review["time"] = datetime.utcnow().isoformat()
            review["dealerId"] = dealer_id
            review["review"] = request.POST["content"]
            review["name"] = request.user.username
            if request.POST['purchasecheck'] == "on":
                review["purchase"] = True 
            else:
                review["purchase"] = False
                review["purchase_date"]= request.POST["purchasedate"]
                review["car_make"] = models.carmake.name
                review["car_model"] = models.carmodel.name
                review["car_year"]= models.carmodel.year.strftime("%Y")

                json_payload = {}
                json_payload = review
                print (json_payload)
                
                response = post_request(url, json_payload, params=review)
            return redirect('djangoapp:dealer_details', dealer_id=dealer_id)
        else:
            return HttpResponse("Invalid Request type: " + request.method)
    else:
        return HttpResponse("User not authenticated")
