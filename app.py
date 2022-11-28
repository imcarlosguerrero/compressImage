#Create a flask app
from flask_ngrok import run_with_ngrok
from flask import Flask, render_template, request, session, redirect, url_for

import numpy as np
from PIL import Image

from flask_session import Session

UPLOAD_FOLDER = '/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = 'hardcoding is bad'
sess = Session()
SESSION_TYPE = 'filesystem'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/compressImage", methods=["POST"])
def compressImage():
    imageToCompress = request.files['imageToCompress']
    imageToCompress.save('imageToCompress.png')
    print(imageToCompress)
    compressionFactor = request.form.get("compressionFactor")
    
    if imageToCompress and allowed_file(imageToCompress.filename):
        
        img = Image.open(imageToCompress)
        imggray = img.convert('LA')
        imgmat = np.array(list(imggray.getdata(band=0)), float)
        imgmat.shape = (imggray.size[1], imggray.size[0])
        imgmat = np.matrix(imgmat)
        
        U, sigma, V = np.linalg.svd(imgmat)
        
        for i in range(5, int(compressionFactor), 5):
            reconstimg = np.matrix(U[:, :i]) * np.diag(sigma[:i]) * np.matrix(V[:i, :])
            
        #Save the image
        img = Image.fromarray(reconstimg)
        img = img.convert('RGB')
        img.save("compressedImage" + compressionFactor + ".png")

        return render_template("index.html", sendMessage=True, mensaje="Imágen comprimida exitosamente")
    else:
        return render_template("index.html", sendMessage=True, mensaje="Extensión de archivo no permitida, solo se permiten archivos .png, .jpg y .jpeg")
