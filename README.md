# Miare Financial Report Project

## General Info
This is a financial reporting system that allows you to generate weekly reports of financial transactions of maire couriers. The system has been built using Django and Django Rest Framework.

## Technologies

- Python
- Django
- DRF
- Sqlite

## Installation
1- Clone the repository
```
git clone https://github.com/shirani98/Miare-Couriers-Income.git
```

2- Change into the project directory
```
cd Miare-Couriers-Income
```
3- Create a virtual environment
```
python3 -m venv venv
```
4- Activate the virtual environment
```
source venv/bin/activate
```
5- Install the dependencies
```
pip install -r requirements.txt
```
6- Run the migrations
```
python manage.py migrate
```
7- Run the server
```
python manage.py runserver
```
## Usage
The system provides an API to retrieve Weekly Reports. The API endpoint can be accessed at http://127.0.0.1:8000/api/.

## Testing
To run the tests, run the following command:
```
python manage.py test
```
