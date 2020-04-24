from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = '/tmp/images'
configure_uploads(app, photos)


class DataObj():
    pass


@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'image' in request.files:
        filename = photos.save(request.files['image'])
        return filename
    return render_template('upload.html', obj=request)


if __name__ == '__main__':
    app.run(debug=True)
