from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES, TEXT, UploadNotAllowed #set file jenis apa yang mau di upload

app = Flask(__name__)

photos = UploadSet('photos', IMAGES) #Bikin object photos nama upload setnya 'photos', jenis filenya image
# photos = UploadSet('photos', IMAGES + TEXT +('py','pyc','cpp')) #kalo mau ada jenis extension macem2 tanpa config allow

app.config['UPLOADED_PHOTOS_DEST'] = 'pictures' #['UPLOADED_(NAMA DI UPLOAD SET)_DEST'] 'pictures' nama folder destinasinya
app.config['UPLOADED_PHOTOS_ALLOW'] = ['txt','py'] #untuk mengizinkan photos upload file lain
app.config['UPLOADED_PHOTOS_DENY'] = ['jpg'] #untuk menolak file image tertentu

configure_uploads(app, photos)

##############################################################
# UPLOADED_FILES_DEST
# This indicates the directory uploaded files will be saved to.
# UPLOADED_FILES_URL
# If you have a server set up to serve the files in this set, this should be the URL they are publicly accessible from. Include the trailing slash.
# UPLOADED_FILES_ALLOW
# This lets you allow file extensions not allowed by the upload set in the code.
# UPLOADED_FILES_DENY
# This lets you deny file extensions allowed by the upload set in the code.
#############################################################

@app.route('/upload', methods=['GET','POST'])
def upload():

    if request.method == 'POST' and 'thefile' in request.files:
        try:
            image_filename = photos.save(request.files['thefile']) #photos dari photos = UploadSet('photos', IMAGES) #thefile dari name input file

            # return '<h1>' +photos.path(image_filename)+ '</h1>'.format(image_filename)
            return '<h1>' +photos.url(image_filename)+ '</h1>'.format(image_filename)
        except UploadNotAllowed:
            return '<h1> File is not Allowed </h1>'

    return render_template('upload.html')





if __name__ == '__main__':
    app.run(debug=True)