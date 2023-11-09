this project is simple CRUD project in Django
for run this project in your localmachine


command:
set a virtualenvironment using python -m venv env
activate virtual env as in windows env/scripts/activate
git clone URL
pip install -r requirements.txt

then 
cd offerproject
python manage.py makemigrations
python manage.py migrate
python manage.py runserver


for checking the routes in postman

for create user
http://127.0.0.1:8000/offer/create_user/
for login user
http://127.0.0.1:8000/offer/token/
for create offer
http://127.0.0.1:8000/offer/

get all offer
http://127.0.0.1:8000/offer/

here we can filter out the offer for your need
like
(offer less than 1000)
http://127.0.0.1:8000/offer/?amount=10000

we can filter offer_type,start_date,end_date,amount

user can update his offer with offer_id

http://127.0.0.1:8000/offer/5/

user can delete his offer with offer_id

user can show all offers he is created