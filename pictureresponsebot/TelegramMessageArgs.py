from typing import Dict
from typing import NewType

from telegram import Bot

TelegramMessageArgs = NewType('TelegramMessageArgs', Dict[str, Bot or int or str or bytes])
