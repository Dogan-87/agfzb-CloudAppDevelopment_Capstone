https://django-fstck-capstoneapp.us-south.cf.appdomain.cloud/djangoapp/

https://djangocapstoneapp.mybluemix.net/djangoapp/

## Project Overwiev

#### 1.The user interacts with the Django application through a web browser.
#### 2.The Django application handles the user authentication using the SQLite database as the persistance layer.
#### 3.The SQLite database also stores the Car Make and the Car Model data.
#### 4.The dealerships and the reviews are stored in Cloudant, a NoSQL document based database.
#### 5.IBM Cloud functions are used to interface with the Cloudant database to get dealerships, get reviews and post reviews.
#### 6.The Django application talks to the IBM Cloud Functions via a set or proxy services.

![](https://user-images.githubusercontent.com/85358503/167597106-68cf879f-a341-44f9-9c5a-09646330cc87.jpg)



# Final Project Template

The final project for this course has several steps that you must complete. 
To give you an overview of the whole project, all the high-level steps are listed below. 
The project is then divided into several smaller labs that give the detailed instructions for each step. 
You must complete all the labs to successfully complete the project.

## Project Breakdown

**Prework: Sign up for IBM Cloud account and create a Watson Natural language Understanding service**
1. Create an IBM cloud account if you don't have one already.
2. Create an instance of the Natural Language Understanding (NLU) service.

**Fork the project Github repository with a project then build and deploy the template project**
1. Fork the repository in your account
2. Clone the repository in the theia lab environment
3. Create static pages to finish the user stories
4. Deploy the application on IBM Cloud

**Add user management to the application**
1. Implement user management using the Django user authentication system.
2. Set up continuous integration and delivery

**Implement backend services**
1. Create cloud functions to manage dealers and reviews
2. Create Django models and views to manage car model and car make
3. Create Django proxy services and views to integrate dealers, reviews, and cars together
 
**Add dynamic pages with Django templates**
1. Create a page that shows all the dealers
2. Create a page that show reviews for a selected dealer
3. Create a page that let's the end user add a review for a selected dealer

**Containerize your application**
1. Add deployment artifacts to your application
2. Deploy your application
