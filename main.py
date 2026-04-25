# ============================================================
# IMPORTACIONES
# ============================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
import re

# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="API Calculador de Valor Final",
    description="Calcula el valor final de un producto con descuento e IVA",
    version="1.0"
)

# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# MODELO (SIN VALIDACIÓN AUTOMÁTICA DE gt/le)
# ============================================================

class Producto(BaseModel):
    codigo: str = Field(..., example="PROD-001")
    nombre: str = Field(..., example="Camisa")
    costo_base: float
    descuento: float
    iva: float

# ============================================================
# VALIDACIÓN MANUAL
# ============================================================

def validar_campos(producto: Producto):

    if not re.match(r'^[a-zA-Z0-9\-]+$', producto.codigo):
        return False, "Código inválido"

    if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', producto.nombre):
        return False, "Nombre inválido"

    return True, ""

# ============================================================
# HOME (evita 404 en /)
# ============================================================

@app.get("/")
def home():
    return {
        "mensaje": "API activa",
        "endpoint": "/calcular/valorfinal"
    }

# ============================================================
# ENDPOINT PRINCIPAL
# ============================================================

@app.post("/calcular/valorfinal")
def calcular_valor_final(producto: Producto):

    # 🔴 VALIDACIÓN PERSONALIZADA (404 QUE QUIERES)
    if producto.costo_base <= 0:
        return JSONResponse(
            status_code=404,
            content={
                "codigo_http": 404,
                "titulo": "Valor no válido",
                "detalle": "El costo base no puede ser negativo o cero",
                "valor_final": 0
            }
        )

    valido, error = validar_campos(producto)

    if not valido:
        return JSONResponse(
            status_code=400,
            content={
                "codigo_http": 400,
                "titulo": "Error de validación",
                "detalle": error,
                "valor_final": 0
            }
        )

    try:
        descuento_pesos = producto.costo_base * (producto.descuento / 100)
        valor_con_descuento = producto.costo_base - descuento_pesos
        iva_pesos = valor_con_descuento * (producto.iva / 100)
        valor_final = valor_con_descuento + iva_pesos

        return {
            "codigo_http": 200,
            "titulo": "Valor Total a Pagar",
            "codigo_producto": producto.codigo,
            "nombre_producto": producto.nombre,
            "valor_base": producto.costo_base,
            "iva_aplicado": producto.iva,
            "descuento_aplicado": producto.descuento,
            "valor_con_descuento": valor_con_descuento,
            "iva_en_pesos": iva_pesos,
            "descuento_en_pesos": descuento_pesos,
            "valor_final": valor_final
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "codigo_http": 500,
                "titulo": "Error interno",
                "detalle": str(e),
                "valor_final": 0
            }
        )
