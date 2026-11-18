# QrGenerator

Aplicación web en Python para generar códigos QR **gratis y sin fecha de caducidad**.

Los códigos generados son *estáticos*: el contenido (URL, texto, WiFi, etc.) va codificado directamente en la imagen y no depende de ningún servidor ni servicio de redirección, por lo que funcionan para siempre.

## Funcionalidades

- Tipos de QR: URL / texto, WiFi, Email, Teléfono y SMS
- Vista previa en vivo mientras se escribe
- Personalización de color, fondo, tamaño del módulo y margen
- Nivel de corrección de errores configurable (L, M, Q, H)
- Descarga en PNG o SVG (vectorial, ideal para impresión)
- Interfaz responsive con modo claro y oscuro

## Tecnologías y librerías

| Librería | Uso |
| --- | --- |
| [Flask](https://flask.palletsprojects.com/) | Servidor web y rutas |
| [qrcode](https://github.com/lincolnloop/python-qrcode) | Generación de la matriz del código QR |
| [Pillow](https://python-pillow.org/) | Renderizado de la imagen PNG |
| HTML, CSS y JavaScript | Interfaz y vista previa en vivo |

Requiere Python 3.10 o superior.

## Estructura

```
├── app.py              # Servidor Flask y generación de QR (PNG/SVG)
├── requirements.txt    # Dependencias
├── templates/
│   └── index.html      # Interfaz web
└── static/
    └── style.css       # Estilos
```

## Instalación

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
