from flask import Flask, render_template, \
  request, send_from_directory, flash, session, url_for, redirect
from flask_uploads import UploadSet, configure_uploads, IMAGES
from model import predict

#https://hackersandslackers.com/flask-application-factory/


def create_app():
    app = Flask(__name__)
    app.secret_key = "super secret key"
    out_path = '/tmp/images/'
    app.config['UPLOADED_PHOTOS_DEST'] = out_path
    photos = UploadSet('photos', IMAGES)
    configure_uploads(app, photos)
    return app, photos

app, photos = create_app()


class DataObj():
    pass


"""
 Check if the file extension is of type IMAGES
 ('jpg jpe jpeg png gif svg bmp'
"""
def checkFileType(f: str):
    return f.split('.')[-1] in IMAGES

def cleanString(v:str):
    out_str = v
    delm = ['_', '-', '.']
    for d in delm:
        out_str = out_str.split(d)
        out_str = " ".join(out_str)
    return out_str

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)


@app.route('/prediction/<filename>', methods=['GET', 'POST'])
def prediction(filename):
    obj = DataObj
    obj.is_image_display = False
    obj.is_predicted = False
    if request.method == 'POST' and filename:
        val = app.config['UPLOADED_PHOTOS_DEST']+filename
        obj.image = filename
        jf = '.' + url_for('static', filename='data/imagenet_class_index.json')
        p = predict(val, jf)
        if len(p) == 2:
            obj.is_image_display = True
            obj.is_predicted = True
            obj.value = cleanString(p[1])
            return render_template('/predict.html', obj=obj)
        else:
            flash(f'Something went wrong with prediction. Try a different image')
    return render_template('/upload.html', obj=obj)

@app.route('/', methods=['GET', 'POST'])
def upload():
    obj = DataObj
    obj.is_image_display = False
    obj.image = ""
    if request.method == 'POST' and 'image' in request.files:
        ft = request.files['image']
        if checkFileType(ft.filename):
            filename = photos.save(request.files['image'])
            obj.image = filename
            session["filename"] = filename
            obj.is_image_display = True
            obj.is_predicted = False
            return render_template('/predict.html', obj=obj)
        else:
            if ft.filename:
                msg = f"{ft.filename} is not an image file"
            else:
                msg = "Please select an image file"
            flash(msg)
        return render_template('/upload.html', obj=obj)
    return render_template('/upload.html', obj=obj)

if __name__ == '__main__':
    app.run(debug=True)
