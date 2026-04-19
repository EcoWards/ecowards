import os
import mysql.connector
import pytz
from datetime import datetime
from flask import Flask
app = Flask(__name__)

zona = pytz.timezone("America/El_Salvador")
datetime.now(zona)

conn = mysql.connector.connect(
    host=os.getenv("MYSQLHOST") or "localhost",
    user=os.getenv("MYSQLUSER") or "root",
    password=os.getenv("MYSQLPASSWORD") or "",
    database=os.getenv("MYSQLDATABASE") or "",
    port=int(os.getenv("MYSQLPORT") or 3306)
)

cursor = conn.cursor()

# 🗄️ CREAR TABLA SI NO EXISTE
cursor.execute("""
CREATE TABLE IF NOT EXISTS reciclaje (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(100),
    material VARCHAR(50),
    cantidad INT,
    puntos INT,
    fecha DATETIME
)
""")

conn.commit()

# 🎯 PUNTOS POR MATERIAL
materiales = {
    "carton": 3,
    "lata": 5,
    "plastico": 4,
    "papel": 2
}

# ➕ REGISTRAR RECICLAJE
def registrar(usuario, material, cantidad):
    material = material.lower()

    if material not in materiales:
        return "Material inválido"

    puntos = materiales[material] * cantidad

    cursor.execute("""
        INSERT INTO reciclaje (usuario, material, cantidad, puntos, fecha)
        VALUES (%s, %s, %s, %s, %s)
    """, (usuario, material, cantidad, puntos, datetime.now()))

    conn.commit()

    return f"{usuario} ganó {puntos} puntos"

# 📊 VER PUNTOS
def ver_puntos(usuario):
    cursor.execute("""
        SELECT SUM(puntos) FROM reciclaje WHERE usuario = %s
    """, (usuario,))
    
    resultado = cursor.fetchone()[0]
    return resultado if resultado else 0

# 📈 RANKING
def ranking():
    cursor.execute("""
        SELECT usuario, SUM(puntos) as total
        FROM reciclaje
        GROUP BY usuario
        ORDER BY total DESC
    """)
    return cursor.fetchall()

# 🔥 EJECUCIÓN AUTOMÁTICA (Railway necesita esto)
print("Servidor iniciado correctamente")

@app.route("/")
def home():
    return "Servidor funcionando 🚀"

# 🔹 PING
@app.route("/ping")
def ping():
    return "pong"

# 🔹 TEST (AQUÍ VA EL INSERT)
@app.route("/test")
def test():
    try:
        cursor.execute("""
            INSERT INTO reciclaje (usuario, material, cantidad, puntos, fecha)
            VALUES (%s, %s, %s, %s, %s)
        """, ("Rodrigo", "carton", 2, 6, datetime.now()))

        conn.commit()

        return "INSERT OK ✅"

    except Exception as e:
        return f"ERROR: {str(e)}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))