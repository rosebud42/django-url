# URL Shortener and Encryptor

A Django-based web application that allows users to shorten and encrypt URLs. Users can manage the lifecycle of the shortened links by setting them to be valid for a single use or until a specified expiration date. Additionally, users can edit the properties of their shortened links and view all created links in one place.


## Features

- **Shorten a URL**: Navigate to the main page, input your URL, and submit the form to get a shortened link.

- **Encrypt a URL**: Set a password during the URL shortening process to secure the link.

- **Configure Validity**: Choose whether the link should be valid for a single use or set an expiration date.

- **Edit Links**: Access the edit page to modify link properties such as password, expiration date, and comments.

- **View All Links**: Go to the 'Show All' section to see a list of all your created links.

## Installation

1. Clone the repository:
   - `git clone https://github.com/rosebud42/django-url.git`

2. **Install the dependencies:**
   - `pip install -r requirements.txt`

3. **Navigate to the project directory:**
   - `cd url-shortener`

4. **Apply migrations:**
   - `python manage.py migrate`

5. **Run the application:**
   - `python manage.py runserver`

# Made by rosebud. Bugs are features..
# contact : efekanaksoy35@gmail.com

