#Create a flask app

from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
import deployDevContainer

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.secret_key = 'hardcoding is bad'
sess = Session()
SESSION_TYPE = 'filesystem'

@app.route("/", methods=["GET"])
def index():
    if(session.get('mensaje', "no set") == "no set"):
        return render_template("index.html")
    else:
        mensaje = session["mensaje"]
        session.clear()
        return render_template("index.html", sendMessage = True, mensaje=mensaje)

@app.route("/createContainer", methods=["POST"])
def createContainer():
    containerImage = str(request.form.get("containerImage"))
    containerName = str(request.form.get("containerName"))
    containerMemory = str(request.form.get("containerMemory"))
    containerCPU = str(request.form.get("containerCPU"))
    containerPassword = str(request.form.get("containerPassword"))
    print(containerImage, containerName, containerMemory, containerCPU, containerPassword)
    session['mensaje'] = deployDevContainer.createContainer(containerName, containerImage, containerMemory, containerCPU, containerPassword)
    return redirect(url_for("index"))
