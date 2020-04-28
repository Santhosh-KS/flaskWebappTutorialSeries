# start.sh

export FLASK_APP=wsgi.py
export FLASK_DEBUG=1
export APP_CONFIG_FILE=config.py
export UPLOADED_PHOTOS_DEST=/tmp/images/
export SECRET_KEY="abcd"
flask run
