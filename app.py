from flask import Flask

from flask import render_template
from flask import request

import pusher

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("app.html")

@app.route("/alumnos")
def alumnos():
    return render_template("alumnos.html")

@app.route("/alumnos/guardar", methods=["POST"])
def alumnosGuardar():
    matricula      = request.form["txtMatriculaFA"]
    nombreapellido = request.form["txtNombreApellidoFA"]
    return f"Matrícula {matricula} Nombre y Apellido {nombreapellido}"

@app.route("/registrar", methods=["GET"])
def evento():
    pusher_client = pusher.Pusher(
        app_id = "1867154"
        key = "84b47e81b86f0dd58c26"
        secret = "a1408f8b96c7eba73b16"
        cluster = "us2"
        ssl=True
    )
    
    pusher_client.trigger("canalRegistrosTemperatura", "registroTemperatura", {})