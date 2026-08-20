from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="API Verificación QR",
    description="Devuelve el estado de códigos QR",
    version="1.0.0"
)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

class RespuestaQR(BaseModel):
    exito: bool
    mensaje: str
    codigo: str | None = None
    estado: str
    fecha_expiracion: str | None = None

@app.get("/api/verificar-qr/{codigo_qr}", response_model=RespuestaQR)
def verificar_qr(codigo_qr: str):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT codigo, estado, fecha_expiracion FROM codigos_qr WHERE codigo = %s", (codigo_qr,))
        qr = cursor.fetchone()

        if not qr:
            return RespuestaQR(exito=False, mensaje="Código QR no registrado", estado="no_existe")

        estado_actual = qr["estado"]
        fecha_exp = qr["fecha_expiracion"]

        if fecha_exp:
            fecha_obj = datetime.fromisoformat(str(fecha_exp)) if isinstance(fecha_exp, str) else fecha_exp
            if datetime.now() > fecha_obj and estado_actual == "activo":
                cursor.execute("UPDATE codigos_qr SET estado = 'vencido' WHERE codigo = %s", (codigo_qr,))
                conn.commit()
                estado_actual = "vencido"

        return RespuestaQR(exito=True, mensaje="Consulta exitosa", codigo=qr["codigo"], estado=estado_actual, fecha_expiracion=str(fecha_exp))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)