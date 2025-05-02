2.Run and build instructions:
 Step 1: Install Required Software
Python 3.12 or later
SQLite (comes built-in with Python) 
Flask and necessary Python libraries
IDE such as Visual Studio Code or PyCharm for development
Step 2: set up environment:
Open the project folder (Book_Smart_Hotel) in IDE .
It's just an option to create the venv.
Create and activate a Python virtual environment:
python -m venv venv
venv\Scripts\activate  (for Windows)
source venv/bin/activate  (for macOS/Linux)
Step 3: Install Project Dependencies
Using the following commands install necessary dependencies:
Pip install flask
Pip install flask-sqlalchemy
Pip install flask-mail
Pip install flask-login
Step 4: Start the Flask Server
Run the main application file to start the server:
python main.py
(If python3 is needed on your system: python3 main.py)
Step 5: Access the Application
Open your browser and go to:
http://127.0.0.1:5000
You should see the homepage of the Book Smart Hotel booking system.
Step 6: Test the System Features
Register as a new user or login as admin.
Search for available rooms.
Make bookings and view booking details.
Admin can manage room availability and view customer bookings.
