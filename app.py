from __future__ import annotations

import mimetypes
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

from flask import Flask, abort, jsonify, send_from_directory

ROOT = Path(__file__).resolve().parent
SITE_DIR = ROOT / "site"
DOWNLOADS_DIR = ROOT / "downloads"

CATEGORIES = {
    "application": "Uygulama",
    "updates": "Güncellemeler",
    "tools": "Araçlar",
    "extras": "Ek içerikler",
}

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024 * 1024


def human_size(size: int) -> str:
    value = float(size)
    for unit in ("B", "KB", "MB", "GB"):
        if value < 1024 or unit == "GB":
            return f"{value:.0f} {unit}" if unit == "B" else f"{value:.1f} {unit}"
        value /= 1024
    return f"{value:.1f} GB"


def get_downloads() -> list[dict]:
    items: list[dict] = []
    for category, label in CATEGORIES.items():
        folder = DOWNLOADS_DIR / category
        folder.mkdir(parents=True, exist_ok=True)
        for path in sorted(folder.iterdir(), key=lambda item: item.stat().st_mtime, reverse=True):
            if not path.is_file() or path.name.startswith("."):
                continue
            stat = path.stat()
            extension = path.suffix.lower().lstrip(".") or "file"
            items.append({
                "name": path.name,
                "category": category,
                "category_label": label,
                "extension": extension.upper(),
                "size": human_size(stat.st_size),
                "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%d.%m.%Y"),
                "download_url": f"/download/{category}/{quote(path.name)}",
            })
    return items


@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    if response.mimetype in {"text/html", "application/json"}:
        response.headers["Cache-Control"] = "no-store"
    return response


@app.get("/")
def home():
    return send_from_directory(SITE_DIR, "index.html")


@app.get("/api/health")
def health():
    return jsonify({"ok": True, "name": "NEXUS FPS"})


@app.get("/api/downloads")
def downloads_api():
    return jsonify({"downloads": get_downloads()})


@app.get("/download/<category>/<path:filename>")
def download_file(category: str, filename: str):
    if category not in CATEGORIES:
        abort(404)

    category_root = (DOWNLOADS_DIR / category).resolve()
    candidate = (category_root / filename).resolve()
    try:
        candidate.relative_to(category_root)
    except ValueError:
        abort(404)

    if not candidate.is_file():
        abort(404)

    return send_from_directory(
        category_root,
        candidate.relative_to(category_root).as_posix(),
        as_attachment=True,
        download_name=candidate.name,
        mimetype=mimetypes.guess_type(candidate.name)[0] or "application/octet-stream",
        conditional=True,
    )


@app.get("/<path:asset_path>")
def site_assets(asset_path: str):
    target = (SITE_DIR / asset_path).resolve()
    try:
        target.relative_to(SITE_DIR.resolve())
    except ValueError:
        abort(404)
    if not target.is_file():
        abort(404)
    return send_from_directory(SITE_DIR, asset_path, conditional=True)


if __name__ == "__main__":
    # Local preview only. Public hosting uses Gunicorn and the PORT variable.
    import os

    from werkzeug.serving import run_simple

    run_simple("127.0.0.1", int(os.environ.get("PORT", "8000")), app, use_reloader=False)
