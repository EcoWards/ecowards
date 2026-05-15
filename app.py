from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import mysql.connector
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# =========================
# MYSQL
# =========================
def get_db():

    conn = mysql.connector.connect(
        host=os.environ.get("MYSQLHOST"),
        user=os.environ.get("MYSQLUSER"),
        password=os.environ.get("MYSQLPASSWORD"),
        database=os.environ.get("MYSQLDATABASE"),
        port=int(os.environ.get("MYSQLPORT"))
    )

    return conn, conn.cursor(dictionary=True)

# =========================
# CREAR TABLAS
# =========================
try:

    conn, cursor = get_db()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) UNIQUE,
        password VARCHAR(100),
        nombre VARCHAR(100),
        ecoCoins INT DEFAULT 0,
        objetos INT DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historial (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100),
        accion TEXT,
        fecha DATETIME
    )
    """)

    cursor.execute("""
    INSERT IGNORE INTO users(username, password, nombre, ecoCoins, objetos)
    VALUES
    ('carlos_000145', '1234', 'Carlos', 1000, 50),
    ('alfonso_000110', '1234', 'Alfonso', 60, 20)
    """)

    conn.commit()
    conn.close()

    print("✅ MySQL conectado")

except Exception as e:
    print("❌ Error MySQL:", e)

# =========================
# REWARDS
# =========================
rewards = [
    {"id": 1, "nombre": "Snickers", "costo": 100},
    {"id": 2, "nombre": "Chicle", "costo": 50},
    {"id": 3, "nombre": "Paleta", "costo": 400},
    {"id": 4, "nombre": "Almuerzo", "costo": 1000},
    {"id": 5, "nombre": "Cine", "costo": 1300},
    {"id": 6, "nombre": "1 Hora Well", "costo": 2500}
]

# =========================
# LOGIN
# =========================
@app.route("/api/login", methods=["POST"])
def login():

    try:

        data = request.json

        username = data.get("username")
        password = data.get("password")

        conn, cursor = get_db()

        cursor.execute("""
            SELECT *
            FROM users
            WHERE username=%s AND password=%s
        """, (username, password))

        user = cursor.fetchone()

        conn.close()

        if not user:
            return jsonify({
                "error": "Usuario o contraseña incorrectos"
            }), 401

        return jsonify({
            "success": True,
            "username": user["username"],
            "nombre": user["nombre"]
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

# =========================
# USER
# =========================
@app.route("/api/user/<username>")
def get_user(username):

    try:

        conn, cursor = get_db()

        cursor.execute("""
            SELECT nombre, ecoCoins, objetos
            FROM users
            WHERE username=%s
        """, (username,))

        user = cursor.fetchone()

        conn.close()

        if not user:
            return jsonify({
                "error": "Usuario no encontrado"
            }), 404

        return jsonify(user)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

# =========================
# HISTORIAL
# =========================
@app.route("/api/historial/<username>")
def historial(username):

    try:

        conn, cursor = get_db()

        cursor.execute("""
            SELECT accion
            FROM historial
            WHERE username=%s
            ORDER BY fecha DESC
        """, (username,))

        datos = cursor.fetchall()

        conn.close()

        return jsonify([x["accion"] for x in datos])

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

# =========================
# REWARDS
# =========================
@app.route("/api/rewards")
def get_rewards():
    return jsonify(rewards)

# =========================
# RANKING
# =========================
@app.route("/api/ranking")
def ranking():

    try:

        conn, cursor = get_db()

        cursor.execute("""
            SELECT nombre, ecoCoins
            FROM users
            ORDER BY ecoCoins DESC
        """)

        datos = cursor.fetchall()

        conn.close()

        ranking = []

        for x in datos:
            ranking.append({
                "nombre": x["nombre"],
                "puntos": x["ecoCoins"]
            })

        return jsonify(ranking)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

# =========================
# RECICLAR
# =========================
@app.route("/api/reciclar", methods=["POST"])
def reciclar():

    try:

        data = request.json

        username = data["username"]
        tipo = data["tipo"]
        cantidad = int(data["cantidad"])

        materiales = {
            "botella": 3,
            "lata": 4,
            "papel": 1,
            "carton": 2
        }

        if tipo not in materiales:
            return jsonify({
                "error": "Material inválido"
            }), 400

        ecoCoins = materiales[tipo] * cantidad

        conn, cursor = get_db()

        cursor.execute("""
            UPDATE users
            SET ecoCoins = ecoCoins + %s,
                objetos = objetos + %s
            WHERE username=%s
        """, (ecoCoins, cantidad, username))

        accion = f"{cantidad} {tipo}(s) +{ecoCoins} EcoCoins"

        cursor.execute("""
            INSERT INTO historial(username, accion, fecha)
            VALUES(%s, %s, %s)
        """, (username, accion, datetime.now()))

        conn.commit()

        cursor.execute("""
            SELECT *
            FROM users
            WHERE username=%s
        """, (username,))

        user = cursor.fetchone()

        conn.close()

        return jsonify({
            "mensaje": f"Ganaste {ecoCoins} EcoCoins",
            "user": user
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

# =========================
# CANJEAR
# =========================
@app.route("/api/canjear", methods=["POST"])
def canjear():

    try:

        data = request.json

        username = data["username"]
        reward_id = data["rewardId"]

        reward = next(
            (r for r in rewards if r["id"] == reward_id),
            None
        )

        if not reward:
            return jsonify({
                "error": "Reward no encontrado"
            }), 404

        conn, cursor = get_db()

        cursor.execute("""
            SELECT ecoCoins
            FROM users
            WHERE username=%s
        """, (username,))

        user = cursor.fetchone()

        if user["ecoCoins"] < reward["costo"]:

            conn.close()

            return jsonify({
                "error": "No tienes suficientes EcoCoins"
            }), 400

        nuevo = user["ecoCoins"] - reward["costo"]

        cursor.execute("""
            UPDATE users
            SET ecoCoins=%s
            WHERE username=%s
        """, (nuevo, username))

        accion = (
            f"Canjeaste "
            f"{reward['nombre']} "
            f"-{reward['costo']} EC"
        )

        cursor.execute("""
            INSERT INTO historial(username, accion, fecha)
            VALUES(%s, %s, %s)
        """, (username, accion, datetime.now()))

        conn.commit()

        conn.close()

        return jsonify({
            "mensaje": "Canje exitoso"
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

# =========================
# FRONTEND
# =========================
@app.route("/")
def index():
    return send_from_directory(".", "login.html")

@app.route("/<path:path>")
def static_files(path):

    if os.path.exists(path):
        return send_from_directory(".", path)

    return "Archivo no encontrado", 404

# =========================
# RUN
# =========================
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )