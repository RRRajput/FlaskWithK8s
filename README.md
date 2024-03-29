# Flask with K8s

# Introduction

This project was done as part of interview assessment for a company. 
The problem statement can be found in the file `problem_statement.txt`.

The following libraries are needed to run this code:

- sqlalchemy
- flask

To run the code, just run the main.py

GET requests can be made directly from the browser.
POST requests can be made using PostMan.

GET requests are used for generating statistics.

POST requests are used by customers to input data.

# Some comments

I've tried to keep the code minimal and have not added any functionality that is not required. 

I tried to name the variables and methods to the best of my abilities, their intent should be clear by their names. However, if you feel that they're not named well, please help me improve. 

Moreover, I tried to write the code in such a way that comments are not required (for the most part). However, if there's some part of code that you don't understand, let me know.

For generating statistics, currently we only support one date format (i.e. dd-mm-yyyy).

This is the first time I've used flask so the code for flask might not be very good. If it is helpful, you can also have a look at the commit history to see what kind of problems I faced and how did I tackle them.

The k8s deployment could be improved by:
- Putting the postgres authentication as a secret rather than as a config file.
- The Azure Disk resource URI could be put as a secret.

# Architecture

# REST API with flask
As explained above, we only required the GET and the POST requests. 
GET requests are used for generating statistics.
POST requests are used by customers to input data

# Chain of Responsibility Design Pattern to check the incoming requests
I've used chain of responsibility to perform different checks during the evaluation of input data. This allows us to flexibly add new checks if we need them at a later point.

I've diverged a bit from the traditional chain of responsbility by also adding a failure handler (which registers the invalid request) in case the request is invalid AND we can determine which customer sent it.

You can see the chain of commands for both both user requests and statistics generator in the main.py file.

# References
https://refactoring.guru/design-patterns/chain-of-responsibility/python/example

https://pythonbasics.org/flask-rest-api/

Google and Stack overflow
