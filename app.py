import sqlite3
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
DB_PATH = "codigos_qr.db"


def preparar_base_datos():
    """Asegura que exista la columna 'estado' en la tabla 'qrs'"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "ALTER TABLE qrs ADD COLUMN estado TEXT DEFAULT 'DISPONIBLE'"
        )
        conn.commit()
    except sqlite3.OperationalError:
        pass  # La columna ya existe
    conn.close()


@app.route("/")
def index():
    return render_template("escanear.html")


@app.route("/api/validar", methods=["POST"])
def validar_qr():
    datos = request.get_json()
    contenido_qr = datos.get("codigo", "").strip()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Buscar el QR en la base de datos
    cursor.execute(
        "SELECT id, estado FROM qrs WHERE contenido = ?", (contenido_qr,)
    )
    resultado = cursor.fetchone()

    if not resultado:
        conn.close()
        return jsonify(
            {
                "status": "error",
                "mensaje": "❌ CÓDIGO INVÁLIDO: No existe en el sistema.",
            }
        )

    qr_id, estado = resultado

    if estado == "USADO":
        conn.close()
        return jsonify(
            {
                "status": "warning",
                "mensaje": f"⚠️ ALERTA: El boleto ({contenido_qr}) YA FUE UTILIZADO.",
            }
        )

    # Marcar como USADO
    cursor.execute("UPDATE qrs SET estado = 'USADO' WHERE id = ?", (qr_id,))
    conn.commit()
    conn.close()

    return jsonify(
        {
            "status": "exito",
            "mensaje": f"✅ ACCESO PERMITIDO: Boleto válido ({contenido_qr}).",
        }
    )


if __name__ == "__main__":
    preparar_base_datos()
    app.run(host="0.0.0.0", port=5000, debug=True)