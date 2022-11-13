import os


up_dir = os.path.join(os.getcwd(), 'uploaded_file')

if not os.path.exists(up_dir):
    os.mkdir(up_dir)


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'some-special-secret-key'
    UPLOAD_FOLDER = up_dir
