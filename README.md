# Sharefest SMS service [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![SharefestSMS https://polar-dusk-09970.herokuapp.com/](https://img.shields.io/website-up-down-green-red/http/shields.io.svg)](https://polar-dusk-09970.herokuapp.com/)

Sharefest SMS service is a simple Django web app used to broadcast SMS
messages to clients or food pantries

<p align="center">
  <img src="./images/sharefest_home01.png" width="738">
</p>

* This project uses twilio messaging service client to send messages to clients
  based on their zipcode and whether they are a pantry or a community member
<p align="center">
  <img src="./images/sharefest_compose01.png" width="738">
</p>

* accepts .csv files of contacts into a SQLite database
<p align="center">
  <img src="./images/sharefest_upload01.png" width="738">
</p>

* Contact .csv files should contain at least the following information
  **firstname, lastname, email, phonenumber, zipcode, isPantry**


## What does sharefest SMS depend on?
* [Django3.0](https://docs.djangoproject.com/en/3.0/)
* [django-phone-field](https://pypi.org/project/django-phone-field/)
* [Twilio](https://www.twilio.com/docs/libraries/python)
* [Python3.x](https://www.python.org)
* [PostgreSQL](https://www.postgresql.org/)

## Config

1. Clone the repo

2. after installing Django and site dependencies, navigate to 
   the root folder run
   ```sh
   $ python manage.py runserver
   ```
   this will start the server at your local host, django runs on port 8000 by default.

3. 127.0.0.1/admin will bring you to the Admin panel

### Site Structure
Django is a simple  and clean python web app framework.
The structure of the app follows a simple pattern
<details><summary><b>Show details</b></summary>
I have outlined the most relative parts of our app
```
sharefest/
    manage.py 
    
    sharefest/     <--- our site manager folder
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
    sms/            <--- location of sms service and web pages
        static/css
            styles.css
        admin.py
        apps.py
        forms.py    <--- forms for collecting input
        models.py   <--- location of DB models
        urls.py     <--- routes for our site
        views.py    <--- where the data processing happens
        messaging.py <-- contains helper functions
    templates/      <--- this folder contains the html
        baseGeneric.html
        compose.html
        upload.html
        ...
    README.md <--- you are looking at it
</details>

## How to use?
This main functionality site was designed to be as simple as possible
There are not too many moving parts:
you can log in, upload csv files, and send messages

* When sending messages, if you input 00000 to the ZIP code field, you will get all contacts (the pantry filter still applies) 

## Contribute
As with all things, this site could be improved.
Here are some things I'd like to do:
* Security review (always and forever)
* More complete testing
* Better styling 
* Client editing portal? 
*(currently it is easier to manipulate client record with a tool that churches and local pantries seem to commonly use. That software charges rather exorbitantly for messaging)*


any proposed contributions or pull requests should be made to
[this github](https://github.com/mongoosePK/Share-Fest-1)

### License
Copyright 2020 William Pulkownik

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

<!-- BADGES
[![Website sharefest.sms.service.not](https://img.shields.io/website-up-down-green-red/http/myfakewebsitethatshouldnotexist.at.least.i.hope.svg)](http://sharefest.sms.service.not/)

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) 

END BADGES -->
