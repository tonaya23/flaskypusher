from flask import Flask, render_template, request
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
    con.close()

    return registros

@app.route("/registrar", methods=["POST"])
def registrar():
    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()

    telefono = request.form.get("telefono")
    archivo = request.form.get("archivo")

    sql = "INSERT INTO tst0_cursos_pagos (Telefono, Archivo) VALUES (%s, %s)"
    val = (telefono, archivo)
    cursor.execute(sql, val)
    
    con.commit()
    con.close()

    pusher_client = pusher.Pusher(
        app_id = "1867154",
        key = "84b47e81b86f0dd58c26",
        secret = "a1408f8b96c7eba73b16",
        cluster = "us2",
        ssl=True
    )

    pusher_client.trigger("canal_cursos_pagos", "nuevo_curso_pago", {
        "telefono": telefono,
        "archivo": archivo
    })

    return "Registro exitoso", 200

if __name__ == "__main__":
    app.run(debug=True)