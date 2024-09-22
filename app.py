from flask import Flask, render_template, request
import pusher
import mysql.connector
import datetime
import pytz
from flask import jsonify

# Configuración de la conexión a la base de datos
con = mysql.connector.connect(
  host="185.232.14.52",
  database="u760464709_tst_sep",
  user="u760464709_tst_sep_usr",
  password="dJ0CIAFF="
)

# Configuración de Pusher
pusher_client = pusher.Pusher(
    app_id="1867154",
    key="84b47e81b86f0dd58c26",
    secret="a1408f8b96c7eba73b16",
    cluster="us2",
    ssl=True
)

@app.route("/")
def index():
    return render_template("app.html")

@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tst0_cursos_pagos ORDER BY Id_Curso_Pago DESC")
    registros = cursor.fetchall()
    con.close()
    return jsonify(registros)

@app.route("/registrar", methods=["GET"])
def registrar():
    args = request.args
    
    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()

    sql = "INSERT INTO tst0_cursos_pagos (Telefono, Archivo) VALUES (%s, %s)"
    val = (args.get("telefono"), args.get("archivo"))
    cursor.execute(sql, val)
    
    new_id = cursor.lastrowid
    
    con.commit()
    con.close()

    # Trigger Pusher event
    pusher_client.trigger("canalCursosPagos", "nuevoCursoPago", {
        "id": new_id,
        "telefono": args.get("telefono"),
        "archivo": args.get("archivo")
    })

    return jsonify({"message": "Registro insertado correctamente", "id": new_id})

if __name__ == "__main__":
    app.run(debug=True)

    return f"Registro insertado: ID {new_id}, Teléfono {args.get('telefono')}, Archivo {args.get('archivo')}"