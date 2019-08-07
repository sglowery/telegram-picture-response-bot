import logging as logger
from typing import Callable, NoReturn, Any, Optional

from telegram import Bot

from pictureresponsebot import config as config


def call_and_log(func: Callable) -> Callable:
    def _wrapped(*args, **kwargs) -> Optional[Any]:
        log: str = " ".join((func.__name__, "called"))
        logger.info(log)
        return func(*args, **kwargs)
    return _wrapped


def bot_send_picture(func: Callable) -> Callable:
    def _wrapped(*args, **kwargs) -> NoReturn:
        payload: dict = func(*args, **kwargs)
        send_photo_args: dict = {**payload,
                                 'photo': open(construct_image_path(), 'rb')
                                 }
        Bot.send_photo(**send_photo_args)
    return _wrapped


def construct_image_path():
    return ''.join((config.IMAGE_DIRECTORY, config.IMAGE_NAME))
