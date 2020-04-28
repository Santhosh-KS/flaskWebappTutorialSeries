from flask import render_template, request, send_from_directory, flash, url_for
from .model import predict
from flask import current_app as app
from . import photos


class DataObj():
    pass


def checkFileType(f: str):
    return f.split('.')[-1] in ['jpg', 'jpeg', 'png', 'gif', 'svg', 'bmp']


def cleanString(v: str):
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
        jf = url_for('static', filename='data/imagenet_class_index.json')
        p = predict(val, jf)
        if len(p) == 2:
            obj.is_image_display = True
            obj.is_predicted = True
            obj.value = cleanString(p[1])
            return render_template('/predict.html', obj=obj)
        else:
            flash(f'Something went wrong with prediction. Try a different image')
            return render_template('/predict.html', obj=obj)
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

