from flask import request, abort
from functools import wraps
from config.config import Config
from utils.logger.logger import logger
import logging
import uuid


def global_catch(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except:
            if(Config.IS_DEBUG):
                raise
            error_id = uuid.uuid4()
            logger.info(logging.exception(f"Error id: {error_id}"))
            abort(500, description=f"Application failed with unhandled exception. Contact the support. Error id: {error_id}")
    return decorator