import os
import sqlite3

# Crear carpeta para guardar las imágenes extraídas
os.makedirs("qrs_imagenes", exist_ok=True)

# Obtener la ruta absoluta de la base de datos en la raíz del proyecto
ruta_db = os.path.join(os.path.dirname(__file__), "..", "codigos_qr.db")

conn = sqlite3.connect(ruta_db)
cursor = conn.cursor()

# Detectar tablas existentes
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tablas = cursor.fetchall()

if not tablas:
    print("❌ No se encontraron tablas en codigos_qr.db.")
else:
    nombre_tabla = tablas[0][0]
    print(f"🔎 Extrayendo datos desde la tabla: '{nombre_tabla}'...\n")

    cursor.execute(f"SELECT * FROM {nombre_tabla} LIMIT 20")
    registros = cursor.fetchall()

    guardados = 0
    for reg in registros:
        qr_id = reg[0]
        # Detecta automáticamente los datos binarios del QR (bytes)
        blob = next((val for val in reg if isinstance(val, bytes)), None)

        if blob:
            nombre_archivo = f"qrs_imagenes/QR_{qr_id}.png"
            with open(nombre_archivo, "wb") as f:
                f.write(blob)
            print(f"✅ Guardado: {nombre_archivo}")
            guardados += 1

    if guardados == 0:
        print("⚠️ Se encontró la tabla pero no contenía datos binarios (BLOB) de imágenes.")
    else:
        print("\n🎉 ¡Listo! Revisa la carpeta 'qrs_imagenes' en tu explorador.")

conn.close()