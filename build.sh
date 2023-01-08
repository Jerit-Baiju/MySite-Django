# build.sh
echo "user build start -j"
pip install -r requirements.txt
python manage.py collectstatic
echo "user build end -j"
