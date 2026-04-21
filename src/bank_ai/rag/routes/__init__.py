from __future__ import annotations

from flask import Flask

from .admin import admin_bp
from .api import api_bp
from .health import health_bp
from .web import web_bp


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(health_bp, url_prefix="/health")
    app.register_blueprint(admin_bp, url_prefix="/admin")
