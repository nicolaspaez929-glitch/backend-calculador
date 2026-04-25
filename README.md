# Backend — Calculador de Valor Final

## 📋 Descripción

API desarrollada con FastAPI que calcula el valor final de un producto aplicando descuento e IVA.

## 🚀 Ejecutar en local

uvicorn main:app --host 0.0.0.0 --port 3010 --reload

## 📄 Documentación

Swagger:
http://localhost:3010/docs

## 🔌 Endpoint

POST /calcular/valorfinal

## 📥 Ejemplo de request

{
  "codigo": "PROD-001",
  "nombre": "Camisa",
  "costo_base": 50000,
  "descuento": 10,
  "iva": 19
}

## 📤 Respuesta

200 OK → cálculo correcto  
404 → error en parámetros

## 🌐 Despliegue

Subir esta carpeta a Render como Web Service.