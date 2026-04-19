import os
import mysql.connector
from datetime import datetime

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

@app.route("/test")
def test():
    cursor.execute("""
        INSERT INTO reciclaje (usuario, material, cantidad, puntos, fecha)
        VALUES (%s, %s, %s, %s, %s)
    """, ("Rodrigo", "carton", 2, 6, datetime.now()))

    conn.commit()

    return "Dato insertado"