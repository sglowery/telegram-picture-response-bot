import logging as logger
from typing import Any
from typing import Callable
from typing import Dict
from typing import NoReturn
from typing import Optional

from telegram import Bot


def call_and_log(func: Callable) -> Callable:
    def _wrapped(*args, **kwargs) -> Optional[Any]:
        log: str = f"{func.__name__} called"
        logger.info(log)
        return func(*args, **kwargs)
    return _wrapped


def bot_send_picture(func: Callable) -> Callable:
    def _wrapped(*args, **kwargs) -> NoReturn:
        payload: Dict[str, Any] = func(*args, **kwargs)
        with open(payload.pop('image_path'), 'rb') as f:
            send_photo_args: Dict[str, Any] = {**payload,
                                               'photo': f}
            Bot.send_photo(**send_photo_args)
    return _wrapped


def clamp(num: int, lower: int, upper: int) -> int:
    return lower if num < lower else upper if num > lower else num
