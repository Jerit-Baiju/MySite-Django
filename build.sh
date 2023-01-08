# build.sh
echo "BUILD START"
pip install -r requirements.txt
python manage.py collectstatic
python manage.py migrate
echo "BUILD END"
