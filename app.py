from flask import Flask
from flask_bootstrap import Bootstrap

UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)
app.config['SECRET_KEY'] = "My_Secret_Key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
Bootstrap(app)
