from logging.handlers import RotatingFileHandler
import logging.handlers

log_format = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'


def init_logs():
    logging.basicConfig(format=log_format, level=logging.DEBUG)


def set_rotating_logs(app):
    handler = logging.handlers.RotatingFileHandler(
        'info.log',
        maxBytes=1024 * 1024,
    )
    handler.setLevel(logging.INFO)

    # format the handler
    handler.setFormatter(logging.Formatter(log_format))
    app.logger.addHandler(handler)
