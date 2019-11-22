# simpleSite
A simple site to sign up and retrieve bank information from neonominics.io.Uses google firebase as database. Sign up, sign in and retrieval of bank account information are the features.

HOW TO

Install django by pip install -r requirements.
Then start web server by python manage.py runserver.
127.0.0.1:8000 in the website.
You can use your own neonomics.developer credentials by changing self.client_id and self.client_secret in /apii/apii/bankConn.py.
You must add your firebase database by changing config from /apii/apii/views.py, which can be generated from your own firebase database settings.
