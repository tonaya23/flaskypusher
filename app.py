from flask import Flask
from flask import render_template
from flask import request
import pusher
import mysql.connector
import datetime
import pytz

con = mysql.connector.connect(
  host="185.232.14.52",
  database="u760464709_tst_sep",
  user="u760464709_tst_sep_usr",
  password="dJ0CIAFF="
)

app = Flask(__name__)

@app.route("/")
def index():
    con.close()
    return render_template("app.html")

@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_cursos_pagos")
    
    registros = cursor.fetchall()

    return registros

@app.route("/registrar", methods=["GET"])
def registrar():
    telefono = request.args.get('telefono')
    archivo = request.args.get('archivo')
    
    if telefono and archivo:
        # Insertar en la base de datos
        if not con.is_connected():
            con.reconnect()
        cursor = con.cursor()
        query = "INSERT INTO curso_pago (Telefono, Archivo) VALUES (%s, %s)"
        cursor.execute(query, (telefono, archivo))
        con.commit()
        
        # Obtener el ID del curso recién insertado
        id_curso_pago = cursor.lastrowid
        
        # Configurar Pusher
        pusher_client = pusher.Pusher(
            app_id="1867154",
            key="84b47e81b86f0dd58c26",
            secret="a1408f8b96c7eba73b16",
            cluster="us2",
            ssl=True
        )

        # Enviar los datos a través de Pusher
        pusher_client.trigger("canalRegistrosCursoPago", "registroCursoPago", {
            "Id_Curso_Pago": id_curso_pago,
            "Telefono": telefono,
            "Archivo": archivo
        })

        return f"Registro exitoso. ID: {id_curso_pago}, Teléfono: {telefono}, Archivo: {archivo}"
    else:
        return "Error: Se requieren los parámetros 'telefono' y 'archivo'", 400

    pusher_client.trigger("canalRegistrosCursoPago", "registroCursoPago", request.args)