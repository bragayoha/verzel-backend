from flask_uploads import UploadSet, IMAGES, configure_uploads

images = UploadSet('images', IMAGES)

def configure_uploads(app):
    app.config['UPLOADED_IMAGES_DEST'] = 'uploads/'
    configure_uploads(app, (images,))
