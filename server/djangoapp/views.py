from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarModel
# from .restapis import related methods
from .restapis import get_dealers_from_cf
from .restapis import get_dealer_reviews_by_id_from_cf
from .restapis import post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
# ...
def about(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/contact.html', context)
        
# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login_bootstrap.html', context)
    else: 
        return render(request, 'djangoapp/user_login_bootstrap.html', context)

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/user_registration_bootstrap.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/user_registration_bootstrap.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
#def get_dealerships(request):
#    context = {}
#    if request.method == "GET":
#        return render(request, 'djangoapp/index.html', context)
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://5b09b236.us-south.apigw.appdomain.cloud/api/dealership"
        #url = "https://5b09b236.us-south.apigw.appdomain.cloud/api/dealership?state=California"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context = {"dealerships": get_dealers_from_cf(url)}
        # Concat all dealer's short name
        #dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        #return HttpResponse(dealer_names)
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = 'https://5b09b236.us-south.apigw.appdomain.cloud/api/review'
        url2 = "https://5b09b236.us-south.apigw.appdomain.cloud/api/dealership"
        context = {"reviews":  get_dealer_reviews_by_id_from_cf(url, dealer_id),
                   "dealerships": get_dealers_from_cf(url2),
                   "dealer_id": dealer_id}
        print(dealer_id)
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    context = {}
    # If it is a GET request, just render the add_review page
    if request.method == 'GET':
        url = "https://5b09b236.us-south.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        context = {
            "dealer_id": dealer_id,
            "dealer_name": get_dealers_from_cf(url)[dealer_id-1].full_name,
            "cars": CarModel.objects.all()
        }
        print(context)
        return render(request, 'djangoapp/add_review.html', context)

    if request.method == "POST":

        if request.user.is_authenticated:
            form = request.POST
            review = {
                "name": request.user.first_name + " " + request.user.last_name,
                "dealership": dealer_id,
                "review": form["content"],
                "purchase": form.get("purchasecheck"),
                "id" : request.user.id
                }
            #add review["id"]= 1121
            if form.get("purchasecheck"):
                review["purchase"]=True
                review["purchase_date"] = datetime.strptime(form.get("purchasedate"), "%m/%d/%Y").isoformat()
                print(review)
                print("111")
                print(form)
                print(form['car'])
                car = CarModel.objects.get(pk=form["car"])
                #car = CarModel.objects.get(dealer_id=form["car"])
                print("22")
                review["car_make"] = car.carmake.name
                print("333")
                review["car_model"] = car.name
                print("44")
                review["car_year"]= car.year.strftime("%Y")
                print("55")
            else:
                review["purchase"]=False

            json_payload = {"review": review}
            print (json_payload)
            url = "https://5b09b236.us-south.apigw.appdomain.cloud/api/review"
            post_request(url, json_payload, dealerId=dealer_id)
            print("66")
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
        else:
            return redirect("/djangoapp/login")