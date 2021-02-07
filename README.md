
**App Deployment**

Through Heroku: https://hotel-calisto-backup.herokuapp.com/

**Travis-CI STATUS IMAGE**

[![Build Status](https://travis-ci.com/shrutipanchal7699/CMPE131.svg?branch=master)](https://travis-ci.com/shrutipanchal7699/CMPE131)


#### I. How to run the app:

**1. Prerequisites:** 
Python3, pip and Virtualenv (optional)

**2. Clone our repo:**
Open the terminal/command line, navigate to the directory you want our project in, and enter:

>$ git clone https://github.com/shrutipanchal7699/CMPE131.git

After which, enter the repo

**3. Create a virtual environment (optional):**

>$ python3 -m venv venv

To activate the virtual environment on Mac/Linux:
    
>$ source venv/bin/activate

On Windows:

>$ .\venv\Scripts\activate

**4. Install dependencies:**
>$ pip install -r requirements.txt

**5. Set our environmental variable:**

On Mac/Linux:
>$ export FLASK_APP="HotelApp.py"
>$ export FLASK_DEBUG=1 (optional when debugging)
>$ export MAIL_USERNAME=hotelcallisto131@gmail.com
>$ export MAIL_PASSWORD=hotelcallisto1234!

On Windows:
>$ set FLASK_APP="HotelApp.py"
>$ set FLASK_DEBUG=1 (optional when debugging)
>$ export MAIL_USERNAME=hotelcallisto131@gmail.com
>$ export MAIL_PASSWORD=hotelcallisto1234!

**6. Initiate database file:**
>$ flask db init
>$ flask db migrate
>$ flask db upgrade

**6. Run the app:**
>$ flask run

#### II. Testing:
Test folder: app/tests
To run tests: 
>$ pytest

#### III. Use cases:

**1. Login and Registration**
a. On the homepage, click Menu button on the top right and select "Login or Register"
b. Signup for an account
c. Confirm that user is signed it by checking if "Logout" option is listed in the Menu

**2. Update Password**
a. While logged in, open Menu options and select "My Profile"
b. Enter new password and old password

**3. Create Room (admin)**
a. Go to http://127.0.0.1:5000/admin/room/
b. Click "Create" tab
c. Fill in the input boxes. For example
    Accomodations = "2 beds, 1 bath"
    Room Type = "Regular"
    Price = "200"
    Max Occupants = "2"
    Reservations can be left blank
d. Click Save
e. Add more rooms to get more results for search

**4. Search Room**
a. From the home page:
    Select any date
    Select 1 or 2
    Select Regular
b. Submit
c. Scroll down to check results.

**5. View Room detail**
a. Click a card from the results list, this will take the user to the details
page of that specific room.

**6. Book room**
To book a room, the user must be logged in. However, the user could select the room first before booking.
If the user is not logged in, the user would be prompted to login.
a. From the results, open a card and then click the book button.
b. Also, the user could directly click the book button on the card without opening it.
c. Click submit to finalize the booking process


**7. View Reservation**
To view a reservation, the user must be logged in.
a. Open the menu on the top right, and select "My reservations".

**8. Cancel Reservation**
To cancel a reservation, the user must be logged in.
a. Open the menu on the top right, and select "My reservations".
b. Click cancel on any of the reservations listed.


#### IV. Additional features:
**1. Spanish version**
To change the language, press the flag icon on the top right for the corresponding language desired.

**2. Auto-scroll on submit**
When the user submits parameters for search, the webpage will would auto-scroll to the first result.

**3. Send email to support**
Under the menu
a. Click "Contact us"
b. Fill up the form and submit

**4. Save payment methods**
Under the menu
a. Click "My profile"
b. Click "Payment Methods"
c. Under "Add new payment method," fill up the form
d. Submit



**Extra Note: **

For the sphinx documentation part, uploaded the screenshot of the documentation which was generated before changing the comments.The file name is : sphinx_whenitworked_1.JPG




