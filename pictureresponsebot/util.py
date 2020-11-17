import logging as logger
import os
from typing import Any
from typing import Callable
from typing import NoReturn
from typing import Optional

from telegram import Bot

from pictureresponsebot.TelegramMessageArgs import TelegramMessageArgs


def call_and_log(func: Callable) -> Callable:
    def _wrapped(*args, **kwargs) -> Optional[Any]:
        log = f"{func.__name__} called"
        logger.info(log)
        return func(*args, **kwargs)

    return _wrapped


def bot_send_picture(func: Callable[[Any], Optional[TelegramMessageArgs]]) -> Callable:
    def _wrapped(*args, **kwargs) -> NoReturn:
        payload = func(*args, **kwargs)
        if payload:
            send_photo_args: TelegramMessageArgs = {**payload,
                                                    'photo': os.environ.get('TELEGRAM_FILE_ID')}
            Bot.send_photo(**send_photo_args)

    return _wrapped
