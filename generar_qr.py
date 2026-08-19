import io
import random
import sqlite3
import string
import qrcode

# 1. Configuración de rutas y conexión a la Base de Datos
ruta_bd = "codigos_qr.db"
conn = sqlite3.connect(ruta_bd)
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute("""
    CREATE TABLE IF NOT EXISTS qrs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        contenido TEXT NOT NULL,
        imagen_blob BLOB NOT NULL
    )
""")
conn.commit()


# 2. Función para generar texto aleatorio único
def generar_texto_random(longitud=10):
    caracteres = string.ascii_letters + string.digits
    return "".join(random.choice(caracteres) for _ in range(longitud))


# 3. Función masiva para generar los QR
def generar_qrs_masivos(cantidad):
    print(f"🚀 Iniciando generación de {cantidad} códigos QR aleatorios...\n")

    for i in range(1, cantidad + 1):
        contenido_random = f"QR-{generar_texto_random(10)}"

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(contenido_random)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        imagen_bytes = buffer.getvalue()

        cursor.execute(
            "INSERT INTO qrs (contenido, imagen_blob) VALUES (?, ?)",
            (contenido_random, imagen_bytes),
        )

        if i % 50 == 0 or i == cantidad:
            print(f"✅ Procesados [{i}/{cantidad}] códigos QR...")

    conn.commit()
    print(
        f"\n🎉 ¡Proceso completado! Se han insertado {cantidad} registros de QR en la base de datos."
    )


if __name__ == "__main__":
    CANTIDAD_A_GENERAR = 3000  # Generará 300 registros
    generar_qrs_masivos(CANTIDAD_A_GENERAR)
    conn.close()