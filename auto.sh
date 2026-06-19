
python -m venv venv;
source venv/Scripts/activate;
pip install -r requirements.txt;
python manage.py makemigrations;
python manage.py migrate;

python manage.py createsuperuser
python manage.py runserver