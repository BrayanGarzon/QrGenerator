"""Generador de códigos QR estáticos, gratis y sin caducidad.

Los QR estáticos guardan el contenido directamente en el código (no pasan por
un servidor de redirección), por lo que funcionan para siempre.
"""

import io
import os
import re

import qrcode
from flask import Flask, abort, render_template, request, send_file
from qrcode.constants import ERROR_CORRECT_H, ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q

app = Flask(__name__)

ERROR_LEVELS = {
    "L": ERROR_CORRECT_L,
    "M": ERROR_CORRECT_M,
    "Q": ERROR_CORRECT_Q,
    "H": ERROR_CORRECT_H,
}
HEX_COLOR = re.compile(r"^#[0-9a-fA-F]{6}$")
MAX_DATA_LENGTH = 2000


def escape_wifi(value: str) -> str:
    """Escapa los caracteres especiales del formato WIFI: de los QR."""
    return re.sub(r'([\\;,:"])', r"\\\1", value)


def build_payload(form) -> str:
    """Convierte los campos del formulario en el texto que se codifica en el QR."""
    kind = form.get("type", "text")

    if kind == "wifi":
        ssid = form.get("ssid", "").strip()
        if not ssid:
            abort(400, "El nombre de la red (SSID) es obligatorio.")
        security = form.get("security", "WPA")
        password = form.get("password", "")
        hidden = "true" if form.get("hidden") else "false"
        if security == "nopass":
            return f"WIFI:T:nopass;S:{escape_wifi(ssid)};H:{hidden};;"
        return f"WIFI:T:{security};S:{escape_wifi(ssid)};P:{escape_wifi(password)};H:{hidden};;"

    if kind == "email":
        email = form.get("email", "").strip()
        if not email:
            abort(400, "El correo es obligatorio.")
        subject = form.get("subject", "")
        body = form.get("body", "")
        return f"MATMSG:TO:{email};SUB:{subject};BODY:{body};;"

    if kind == "phone":
        phone = form.get("phone", "").strip()
        if not phone:
            abort(400, "El teléfono es obligatorio.")
        return f"tel:{phone}"

    if kind == "sms":
        phone = form.get("phone", "").strip()
        if not phone:
            abort(400, "El teléfono es obligatorio.")
        return f"SMSTO:{phone}:{form.get('message', '')}"

    text = form.get("text", "").strip()
    if not text:
        abort(400, "Escribe un texto o una URL.")
    return text


def int_in_range(value, default: int, low: int, high: int) -> int:
    try:
        return max(low, min(int(value), high))
    except (TypeError, ValueError):
        return default


def make_qr(form) -> qrcode.QRCode:
    data = build_payload(form)
    if len(data) > MAX_DATA_LENGTH:
        abort(400, f"El contenido es demasiado largo (máx. {MAX_DATA_LENGTH} caracteres).")

    qr = qrcode.QRCode(
        error_correction=ERROR_LEVELS.get(form.get("ecc", "M"), ERROR_CORRECT_M),
        box_size=int_in_range(form.get("box_size"), 10, 4, 40),
        border=int_in_range(form.get("border"), 4, 0, 10),
    )
    qr.add_data(data)
    qr.make(fit=True)
    return qr


def get_colors(form) -> tuple[str, str]:
    fill = form.get("fill", "#000000")
    back = form.get("back", "#ffffff")
    if not HEX_COLOR.match(fill) or not HEX_COLOR.match(back):
        abort(400, "Color inválido.")
    return fill, back


def render_svg(qr: qrcode.QRCode, fill: str, back: str) -> str:
    """Genera un SVG vectorial a partir de la matriz del QR."""
    matrix = qr.get_matrix()  # incluye el borde
    size = len(matrix)
    path = "".join(
        f"M{x},{y}h1v1h-1z"
        for y, row in enumerate(matrix)
        for x, cell in enumerate(row)
        if cell
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" '
        f'width="{size * qr.box_size}" height="{size * qr.box_size}" shape-rendering="crispEdges">'
        f'<rect width="100%" height="100%" fill="{back}"/>'
        f'<path d="{path}" fill="{fill}"/></svg>'
    )


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/qr")
def generate():
    form = request.form
    qr = make_qr(form)
    fill, back = get_colors(form)
    fmt = form.get("format", "png")
    download = form.get("download") == "1"

    if fmt == "svg":
        buffer = io.BytesIO(render_svg(qr, fill, back).encode("utf-8"))
        return send_file(buffer, mimetype="image/svg+xml", as_attachment=download, download_name="qr.svg")

    image = qr.make_image(fill_color=fill, back_color=back).convert("RGB")
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return send_file(buffer, mimetype="image/png", as_attachment=download, download_name="qr.png")


@app.errorhandler(400)
def bad_request(error):
    return {"error": error.description}, 400


if __name__ == "__main__":
    # En macOS el puerto 5000 lo ocupa el Receptor AirPlay, por eso usamos 8765.
    app.run(debug=True, port=int(os.environ.get("PORT", 8765)))
