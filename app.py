from flask import Flask, render_template, request, jsonify
import pusher
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database connection function
def create_db_connection():
    return mysql.connector.connect(
        host="185.232.14.52",
        database="u760464709_tst_sep",
        user="u760464709_tst_sep_usr",
        password="dJ0CIAFF="
    )

# Pusher client
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

@app.route("/buscar", methods=["GET"])
def buscar():
    try:
        con = create_db_connection()
        cursor = con.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tst0_cursos_pagos")
        registros = cursor.fetchall()
        return jsonify(registros)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if con.is_connected():
            cursor.close()
            con.close()

@app.route("/registrar", methods=["POST"])
def registrar():
    data = request.json
    try:
        con = create_db_connection()
        cursor = con.cursor()
        sql = "INSERT INTO tst0_cursos_pagos (Telefono, Archivo) VALUES (%s, %s)"
        val = (data["telefono"], data["archivo"])
        cursor.execute(sql, val)
        con.commit()
        id_curso_pago = cursor.lastrowid
        
        pusher_data = {
            "Id_Curso_Pago": id_curso_pago,
            "Telefono": data["telefono"],
            "Archivo": data["archivo"]
        }
        pusher_client.trigger("canalRegistrosCursoPago", "registroCursoPago", pusher_data)
        
        return jsonify({"message": "Registro creado exitosamente", "id": id_curso_pago}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if con.is_connected():
            cursor.close()
            con.close()

@app.route("/actualizar/<int:id>", methods=["PUT"])
def actualizar(id):
    data = request.json
    try:
        con = create_db_connection()
        cursor = con.cursor()
        sql = "UPDATE tst0_cursos_pagos SET Telefono = %s, Archivo = %s WHERE Id_Curso_Pago = %s"
        val = (data["telefono"], data["archivo"], id)
        cursor.execute(sql, val)
        con.commit()
        
        if cursor.rowcount:
            pusher_data = {
                "Id_Curso_Pago": id,
                "Telefono": data["telefono"],
                "Archivo": data["archivo"]
            }
            pusher_client.trigger("canalRegistrosCursoPago", "actualizacionCursoPago", pusher_data)
            return jsonify({"message": "Registro actualizado exitosamente"}), 200
        else:
            return jsonify({"message": "No se encontró el registro"}), 404
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if con.is_connected():
            cursor.close()
            con.close()

@app.route("/eliminar/<int:id>", methods=["DELETE"])
def eliminar(id):
    try:
        con = create_db_connection()
        cursor = con.cursor()
        sql = "DELETE FROM tst0_cursos_pagos WHERE Id_Curso_Pago = %s"
        val = (id,)
        cursor.execute(sql, val)
        con.commit()
        
        if cursor.rowcount:
            pusher_client.trigger("canalRegistrosCursoPago", "eliminacionCursoPago", {"Id_Curso_Pago": id})
            return jsonify({"message": "Registro eliminado exitosamente"}), 200
        else:
            return jsonify({"message": "No se encontró el registro"}), 404
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if con.is_connected():
            cursor.close()
            con.close()

if __name__ == "__main__":
    app.run(debug=True)