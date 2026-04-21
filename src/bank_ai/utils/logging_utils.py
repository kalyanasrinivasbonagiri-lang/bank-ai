from __future__ import annotations

import logging


def configure_logging(app) -> None:
    logging.basicConfig(
        level=getattr(logging, app.config["LOG_LEVEL"].upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    app.logger.setLevel(app.config["LOG_LEVEL"])
