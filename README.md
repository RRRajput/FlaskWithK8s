# AdexTest

The following libraries are needed to run this code:

- sqlalchemy
- flash

To run the code, just run the main.py

GET requests can be made directly from the browser.
POST requests can be made using PostMan.

GET requests are used for generating statistics.

POST requests are used by customers to input data.

The following design patterns are used:

# Adapter
In this implementation we have used Sqlite for our database. I've used the adapter Design Pattern to make sure that if someone else wants to use a different Database technology, they can do so by just deriving a new class from IDatabaseAdapter. 

# Chain of responsibility
I've used chain of responsibility to perform different checks during the evaluation of input data. This allows us to flexibly add new checks if we need them at a later point.

I've diverged a bit from the traditional chain of responsbility by also adding a failure handler (which registers the invalid request) in case the request is invalid AND we can determine which customer sent it.  

# REST API
As explained above, we only required the GET and the POST requests. 
GET requests are used for generating statistics.
POST requests are used by customers to input data.

# NOTE:

This is the first time I've used flask so the code for flask might not be very great. You can have a look at the commit history to see understand what kind of problems I went through and how did I tackle them.
