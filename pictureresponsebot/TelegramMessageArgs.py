from typing import Dict

from telegram import Bot

TelegramMessageArgs = Dict[str, Bot or int or str or bytes]
