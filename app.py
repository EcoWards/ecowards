import os
import mysql.connector
import pytz
from datetime import datetime
from flask import Flask, request
app = Flask(__name__)

zona = pytz.timezone("America/El_Salvador")

def obtener_fecha():
    return datetime.now(zona).replace(tzinfo=None)

def get_db():
    conn = mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE"),
        port=int(os.getenv("MYSQLPORT") or 3306)
    )
    return conn, conn.cursor()

conn, cursor = get_db()

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
conn.close()

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
    """, (usuario, material, cantidad, puntos, obtener_fecha()))

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

# 🔹 FORMULARIO
@app.route("/form")
def form():
    return """
    <html>
    <head>
        <title>EcoRewards ♻️</title>
        <style>
            body {
                font-family: Arial;
                background: #f4f6f8;
                text-align: center;
            }

            .container {
                background: white;
                padding: 30px;
                margin: 50px auto;
                width: 350px;
                border-radius: 10px;
                box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
            }

            h2 {
                color: #2ecc71;
            }

            input, select {
                width: 90%;
                padding: 10px;
                margin: 10px 0;
                border-radius: 5px;
                border: 1px solid #ccc;
            }

            button {
                background: #2ecc71;
                color: white;
                border: none;
                padding: 10px;
                width: 95%;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
            }

            button:hover {
                background: #27ae60;
            }

            a {
                display: block;
                margin-top: 15px;
                color: #3498db;
                text-decoration: none;
            }

            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>

    <body>
        <div class="container">
            <h2>♻️ EcoWards</h2>

            <form action="/guardar" method="post">
                <input name="usuario" placeholder="Tu nombre" required>

                <select name="material">
                    <option value="carton">Cartón</option>
                    <option value="plastico">Plástico</option>
                    <option value="lata">Lata</option>
                    <option value="papel">Papel</option>
                </select>

                <input name="cantidad" type="number" placeholder="Cantidad" required>

                <button type="submit">Guardar ♻️</button>
            </form>

            <a href="/ranking">Ver Ranking 🏆</a>
        </div>
    </body>
    </html>
    """

# 🔹 GUARDAR
@app.route("/guardar", methods=["POST"])
def guardar():
    try:
        conn, cursor = get_db()  # 🔥 conexión nueva

        usuario = request.form["usuario"]
        material = request.form["material"]
        cantidad = int(request.form["cantidad"])

        puntos = materiales[material] * cantidad

        cursor.execute("""
            INSERT INTO reciclaje (usuario, material, cantidad, puntos, fecha)
            VALUES (%s, %s, %s, %s, %s)
        """, (usuario, material, cantidad, puntos, obtener_fecha()))

        conn.commit()
        conn.close()  # 🔥 cerrar conexión

        return f"{usuario} guardado con {puntos} puntos ✅"

    except Exception as e:
        return f"ERROR: {str(e)}"
    return f"{usuario} guardado con {puntos} puntos"

# 🔹 RANKING
@app.route("/ranking")
def ver_ranking():
    conn, cursor = get_db()

    cursor.execute("""
        SELECT usuario, SUM(puntos) 
        FROM reciclaje 
        GROUP BY usuario 
        ORDER BY SUM(puntos) DESC
    """)
    
    datos = cursor.fetchall()
    conn.close()


    html = """
    <html>
    <head>
        <style>
            body {
                font-family: Arial;
                background: #f4f6f8;
                text-align: center;
            }

            .container {
                background: white;
                padding: 30px;
                margin: 50px auto;
                width: 400px;
                border-radius: 10px;
                box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
            }

            h2 {
                color: #f39c12;
            }

            li {
                list-style: none;
                padding: 10px;
                margin: 5px;
                background: #ecf0f1;
                border-radius: 5px;
            }

            a {
                display: block;
                margin-top: 15px;
                color: #3498db;
                text-decoration: none;
            }
        </style>
    </head>

    <body>
        <div class="container">
            <h2>🏆 Ranking</h2>
            <ul>
    """

    for fila in datos:
        html += f"<li>{fila[0]} - {fila[1]} puntos</li>"

    html += """
            </ul>
            <a href="/form">← Volver</a>
        </div>
    </body>
    </html>
    """

    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))