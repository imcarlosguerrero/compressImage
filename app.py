from flask import Flask, render_template, request, session, redirect, url_for
import numpy as np
from PIL import Image
from flask_session import Session

UPLOAD_FOLDER = '/'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

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
    compressionFactor = request.form.get("compressionFactor")
    
    
    """
    
    Compresion de imagen basada en factorizacion SVD
    
    """
    
    if imageToCompress and allowed_file(imageToCompress.filename):
        
        #Cargado de la imagen
        
        img = Image.open(imageToCompress)
        imggray = img.convert('LA')
        imgmat = np.array(list(imggray.getdata(band=0)), float)
        
        #Shape de la imagen basado en width (1) y height (0)
        
        imgmat.shape = (imggray.size[1], imggray.size[0])
        
        #Conversion de la imagen en una matriz
        
        imgmat = np.matrix(imgmat)
        
        #Descomposicion SVD
        
        U, sigma, V = np.linalg.svd(imgmat)
        
        #Reconstruccion de la matriz haciendo uso de SVD y un factor de compresion para definir cuántos de estos se utilizarán
        
        for i in range(5, int(compressionFactor), 5):
            reconstimg = np.matrix(U[:, :i]) * np.diag(sigma[:i]) * np.matrix(V[:i, :])
            
        #Reconstruccion a formato de imagen a partir de la matriz
        
        img = Image.fromarray(reconstimg)
        img = img.convert('RGB')
        
        #Guardado de la imagen
        
        img.save("compressedImage" + compressionFactor + ".jpg")

        return render_template("index.html", sendMessage=True, mensaje="Imágen comprimida exitosamente")
    else:
        return render_template("index.html", sendMessage=True, mensaje="Extensión de archivo no permitida, solo se permiten archivos .jpg y .jpeg")