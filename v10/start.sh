# start.sh

export FLASK_APP=wsgi.py
export FLASK_DEBUG=1
export APP_CONFIG_FILE=config.py
export UPLOADED_PHOTOS_DEST=/tmp/images/
export SECRET_KEY="abcd"
#waitress-serve --call 'flask_pytorch_web_app:create_app'
gunicorn --bind 0.0.0.0:8000 -w 4 wsgi:app
#flask run
