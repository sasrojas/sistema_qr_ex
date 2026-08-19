import io
import random
import sqlite3
import string
import qrcode

# 1. Configuración de rutas y conexión a la Base de Datos en tu Escritorio
ruta_bd = r"C:\Users\ALISON CASA\Desktop\codigos_qr.db"
conn = sqlite3.connect(ruta_bd)
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute(º
    """
    CREATE TABLE IF NOT EXISTS qrs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        contenido TEXT NOT NULL,
        imagen_blob BLOB NOT NULL
    )
"""
)
conn.commit()


# 2. Función para generar texto aleatorio único
def generar_texto_random(longitud=10):
    caracteres = string.ascii_letters + string.digits
    return "".join(random.choice(caracteres) for _ in range(longitud))


# 3. Función masiva para generar los 300 QR
def generar_qrs_masivos(cantidad):
    print(f"🚀 Iniciando generación de {cantidad} códigos QR aleatorios...\n")

    for i in range(1, cantidad + 1):
        # Crear dato aleatorio único para cada QR
        contenido_random = f"QR-{generar_texto_random(10)}"

        # Crear el objeto QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(contenido_random)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Convertir a bytes para la base de datos
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        imagen_bytes = buffer.getvalue()

        # Insertar registro e imagen en la BD
        cursor.execute(
            "INSERT INTO qrs (contenido, imagen_blob) VALUES (?, ?)",
            (contenido_random, imagen_bytes),
        )

        # Mostrar progreso cada 50 registros para no saturar la pantalla
        if i % 50 == 0 or i == cantidad:
            print(f"✅ Procesados [{i}/{cantidad}] códigos QR...")

    # Guardar todos los cambios en la base de datos
    conn.commit()
    print(
        f"\n🎉 ¡Proceso completado! Se han insertado {cantidad} registros de QR en la base de datos."
    )


# --- EJECUCIÓN DEL SCRIPT ---
if __name__ == "__main__":
    # Definido para generar 3000 QR aleatorios
    CANTIDAD_A_GENERAR = 3000

    generar_qrs_masivos(CANTIDAD_A_GENERAR)

    # Cerrar la conexión al terminar
    conn.close()