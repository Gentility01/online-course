set -o errexit

pip install -r requirements.txt
python manage.py migrate




if [[ $CREATE_SUPERUSER ]];
then
  python world_champ_2022/manage.py createsuperuser --no-input
fi


