python3.9 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
sleep 10
python3.9 manage.py makemigrations
python3.9 manage.py migrate 
python3.9 manage.py collectstatic --noinput