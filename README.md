# Car-Rental-System

A web-based **Car Rental Management System** built with **Python and Django**. The application provides car browsing, user authentication, rental management, payments, and reviews.

## Features

* User registration and login
* Browse and filter available cars
* Car details and images
* Car rental and booking management
* Rental status tracking
* Payment records
* User reviews and ratings
* Django admin panel for management

## Tech Stack

* **Backend:** Python, Django
* **Frontend:** HTML, CSS, JavaScript
* **Database:** MySQL
* **Database Connector:** PyMySQL
* **Image Handling:** Pillow

## Project Structure

```text
carRental/
├── car_rental_app/
├── car_rental_system/
├── media/
├── static/
├── manage.py
├── requirements.txt
└── README.md
```

## Installation

```bash
git clone https://github.com/syedalbasit/carRental.git
cd carRental
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Configure your MySQL database in `settings.py`, then run:

```bash
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.


