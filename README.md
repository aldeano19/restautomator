# **tauto** #
# RESTFUL API TESTER AND AUTOMATOR. #
* Version 1.0

A tool to write, execute and automate, fast and clean, modular test for Restful APIs. The tool allows for creation of low level steps in a Test Case.


###example Scenario: ###
A good way to check a "/create/user" entry point, would be to send a POST to create the user and then send another another POST to retrieve that new user to confirm its creation.

* Step 1: create user -> https://myapi.com/create/user  # if good, continue
* Step 2: retrieve user -> https://myapi.com/create/get # if good, test case success

This two steps would form a test case, they could both be on the same file, **or in separate files to reuse certain steps**.
###example Scenario 2: ###
On our imaginary api assuming that only valid users can create an event, Lets reuse **Step 2** to validate and retrieve the id of the user so that we can create the event.

* Step 2: retrieve user -> https://myapi.com/create/get                          # if good, continue
* Step 3: create event using user id from Step 2 -> https://myapi.com/create/get # if good, continue
* Step 4: retrieve event -> https://myapi.com/event/get                          # if good, test case success


### Set Up ###

* Clone or download this repo.
* Dependencies
    1. python modules: pyyaml, requests. install: ```$ pip install pyyaml requests ``` (may need sudo on linux)

* Extract and navigate to restautomator
* Run sample using ```$ ./tauto OpenWeather/check_name.yaml```

# DOCS #
comming soon...