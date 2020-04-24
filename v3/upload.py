from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
import os

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)

out_path = '/tmp/images/'
app.config['UPLOADED_PHOTOS_DEST'] = out_path
app.config['UPLOADED_PATH'] = out_path
configure_uploads(app, photos)


class DataObj():
    pass


@app.route('/', methods=['GET', 'POST'])
def upload():
    obj = DataObj
    obj.is_image_display = False
    if request.method == 'POST' and 'image' in request.files:
        filename = photos.save(request.files['image'])
        obj.image = '/static/images/'+filename
        os.symlink(out_path + filename, './static/images/'+filename)
        obj.is_image_display = True
        print(f'KSS: {obj.image}')
        return render_template('upload.html', obj=obj)
    return render_template('upload.html', obj=obj)


if __name__ == '__main__':
    app.run(debug=True)
