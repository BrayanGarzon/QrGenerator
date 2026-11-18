# Generador de QR

Web en Python (Flask) para generar códigos QR **gratis y sin fecha de caducidad**.

Los QR son *estáticos*: el contenido (URL, texto, WiFi, etc.) va codificado dentro de la imagen y no depende de ningún servidor, así que funcionan para siempre, incluso si apagas esta aplicación.

## Funciones

- URL / texto, WiFi, Email, Teléfono y SMS
- Vista previa en vivo
- Colores, tamaño, margen y nivel de corrección de errores
- Descarga en PNG o SVG (vectorial, ideal para imprimir)

## Uso

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Abre http://127.0.0.1:8765

> En macOS el puerto 5000 lo usa el Receptor AirPlay (da error 403). Para usar otro puerto: `PORT=9090 python app.py`.
