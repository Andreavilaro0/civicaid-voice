"""Entry point — create Flask app, register blueprints, load models at startup."""

import logging
from flask import Flask
from src.core.config import config
from src.core import cache


def create_app() -> Flask:
    app = Flask(__name__)

    # Configure logging
    logging.basicConfig(level=getattr(logging, config.LOG_LEVEL, logging.INFO))

    # Load cache at startup
    n = cache.load_cache()
    app.logger.info("Loaded %d cache entries", n)

    # Load Whisper model at startup (if enabled)
    if config.WHISPER_ON:
        from src.core.skills.transcribe import load_whisper_model
        load_whisper_model()
        app.logger.info("Whisper model loaded (enabled=%s)", config.WHISPER_ON)

    # Initialize observability hooks
    if config.OBSERVABILITY_ON:
        from src.utils.observability import init_app as obs_init
        obs_init(app)
        app.logger.info("Observability enabled (OTEL_ENDPOINT=%s)", config.OTEL_ENDPOINT or "none")

    # Register blueprints
    from src.routes.health import health_bp
    from src.routes.webhook import webhook_bp
    from src.routes.static_files import static_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(webhook_bp)
    app.register_blueprint(static_bp)

    from src.routes.forget import forget_bp
    app.register_blueprint(forget_bp)

    from src.routes.admin import admin_bp
    app.register_blueprint(admin_bp)

    from src.routes.api_chat import api_bp
    app.register_blueprint(api_bp)

    # Meta WhatsApp Cloud API webhook (registers alongside Twilio)
    from src.routes.webhook_meta import webhook_meta_bp
    app.register_blueprint(webhook_meta_bp)

    # CORS for web frontend API + static audio
    import os
    from flask_cors import CORS
    frontend_origins = os.getenv("FRONTEND_URL", "http://localhost:5173").split(",")
    # Always include GitHub Pages origin for the deployed frontend
    gh_pages = "https://andreavilaro0.github.io"
    if gh_pages not in frontend_origins:
        frontend_origins.append(gh_pages)
    # Include common local dev ports (Vite may use 5173-5180)
    for port in range(5173, 5181):
        local = f"http://localhost:{port}"
        if local not in frontend_origins:
            frontend_origins.append(local)
    CORS(app, resources={
        r"/api/*": {"origins": frontend_origins},
        r"/static/*": {"origins": frontend_origins},
    })

    return app


if __name__ == "__main__":
    import os
    port = int(os.getenv("FLASK_PORT", "5001"))
    app = create_app()
    app.run(host="0.0.0.0", port=port, debug=(config.FLASK_ENV == "development"))
