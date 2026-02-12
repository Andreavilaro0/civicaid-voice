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

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=(config.FLASK_ENV == "development"))
