from flask import Flask, render_template, request, send_from_directory, flash
from flask_uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)
app.secret_key = "super secret key"

photos = UploadSet('photos', IMAGES)

out_path = '/tmp/images/'
stat_image_path = './static/images/'
app.config['UPLOADED_PHOTOS_DEST'] = out_path
configure_uploads(app, photos)

class DataObj():
    pass


"""
 Check if the file extension is of type IMAGES
 ('jpg jpe jpeg png gif svg bmp'
"""
def checkFileType(f: str):
    return f.split('.')[-1] in IMAGES

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)

@app.route('/', methods=['GET', 'POST'])
def upload():
    obj = DataObj
    obj.is_image_display = False
    if request.method == 'POST' and 'image' in request.files:
        ft = request.files['image']
        print(f"KSS {type(ft)}")
        print(f"KSS {ft.filename}")
        if checkFileType(ft.filename):
            filename = photos.save(request.files['image'])
            obj.image = filename
            obj.is_image_display = True
        else:
            flash(f"File : {ft.filename} is not an image file")
        return render_template('upload.html', obj=obj)
    return render_template('upload.html', obj=obj)


if __name__ == '__main__':
    app.run(debug=True)
