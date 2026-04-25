# ============================================================
# IMPORTACIONES
# ============================================================

from fastapi import FastAPI  # Framework principal
from fastapi.middleware.cors import CORSMiddleware  # CORS
from pydantic import BaseModel, Field  # Validación de datos
from fastapi.responses import JSONResponse  # Respuestas personalizadas
import re  # Expresiones regulares

# ============================================================
# CREACIÓN DE LA APP
# ============================================================

app = FastAPI(
    title="API Calculador de Valor Final",
    description="Calcula el valor final de un producto con descuento e IVA",
    version="1.0"
)

# ============================================================
# CONFIGURACIÓN CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes (Hostinger)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# MODELO DE DATOS (VALIDACIÓN AUTOMÁTICA)
# ============================================================

class Producto(BaseModel):
    codigo: str = Field(..., example="PROD-001")
    nombre: str = Field(..., example="Camisa")
    costo_base: float = Field(..., gt=0)
    descuento: float = Field(..., ge=0, le=100)
    iva: float = Field(..., ge=0, le=100)

# ============================================================
# VALIDACIONES PERSONALIZADAS
# ============================================================

def validar_campos(producto: Producto):
    
    # Validar código (alfanumérico con guiones)
    if not re.match(r'^[a-zA-Z0-9\-]+$', producto.codigo):
        return False, "Código inválido"
    
    # Validar nombre (solo letras)
    if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', producto.nombre):
        return False, "Nombre inválido"
    
    return True, ""

# ============================================================
# ENDPOINT PRINCIPAL
# ============================================================

@app.post("/calcular/valorfinal")
def calcular_valor_final(producto: Producto):

    # Validar campos
    valido, error = validar_campos(producto)

    if not valido:
        return JSONResponse(
            status_code=404,
            content={
                "codigo_http": 404,
                "titulo": "Valor no encontrado",
                "valor": 0,
                "detalle": error
            }
        )

    try:
        # ===============================
        # CÁLCULOS
        # ===============================

        descuento_pesos = producto.costo_base * (producto.descuento / 100)

        valor_con_descuento = producto.costo_base - descuento_pesos

        iva_pesos = valor_con_descuento * (producto.iva / 100)

        valor_final = valor_con_descuento + iva_pesos

        # ===============================
        # RESPUESTA EXITOSA
        # ===============================

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
            status_code=404,
            content={
                "codigo_http": 404,
                "titulo": "Valor no encontrado",
                "valor": 0,
                "detalle": str(e)
            }
        )