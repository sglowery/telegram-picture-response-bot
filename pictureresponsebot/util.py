import logging as logger
from typing import Callable, NoReturn, Any, Optional, Dict

from telegram import Bot

from pictureresponsebot import config as config


def call_and_log(func: Callable) -> Callable:
    def _wrapped(*args, **kwargs) -> Optional[Any]:
        log: str = f"{func.__name__} called"
        logger.info(log)
        return func(*args, **kwargs)

    return _wrapped


def bot_send_picture(func: Callable) -> Callable:
    def _wrapped(*args, **kwargs) -> NoReturn:
        payload: Dict[str, Any] = func(*args, **kwargs)
        send_photo_args: Dict[str, Any] = {**payload,
                                           'photo': open(get_image_path(), 'rb')
                                           }
        Bot.send_photo(**send_photo_args)

    return _wrapped


def get_image_path() -> str:
    return f"{config.IMAGE_DIRECTORY}{config.IMAGE_NAME}"


def clamp(num: int, lower: int, upper: int) -> int:
    return lower if num < lower else upper if num > lower else num
