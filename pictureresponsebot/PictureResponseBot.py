import logging
from typing import NoReturn, Iterable, Dict, Any

from telegram import Bot, Update, User
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, Dispatcher

import pictureresponsebot.config as config
from pictureresponsebot.util import call_and_log, bot_send_picture

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


class PictureResponseBot:

    def __init__(self, token: str) -> NoReturn:
        self.token: str = token

    def run(self) -> NoReturn:
        updater: Updater = Updater(self.token)
        dp: Dispatcher = updater.dispatcher
        dp.add_handler(CommandHandler(config.COMMAND_NAME, self.send_picture_from_command))
        dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, self.respond_to_new_members))
        updater.start_polling()
        logging.info("bot is running")
        updater.idle()

    @bot_send_picture
    @call_and_log
    def respond_to_new_members(self, bot: Bot, update: Update) -> Dict[str, Any]:
        human_users: Iterable[User] = self._get_human_users(update.message.new_chat_members)
        response_text: str = ", ".join([user.name for user in human_users])
        welcome_chat: str = config.NEW_USER_REPLY.format(new_member_names=response_text,
                                                         chat_name=update.message.chat.title)
        return self._construct_message_object(bot, update.message.chat.id, welcome_chat)

    @bot_send_picture
    @call_and_log
    def send_picture_from_command(self, bot: Bot, update: Update) -> Dict[str, Any]:
        return self._construct_message_object(bot, update.message.chat.id, config.COMMAND_REPLY,
                                              update.message.message_id)

    @staticmethod
    def _construct_message_object(from_bot: Bot, chat_id: int, caption: str, reply_id: int = None) -> Dict[str, Any]:
        return {'self': from_bot,
                'chat_id': chat_id,
                'caption': caption,
                'reply_id': reply_id}

    @staticmethod
    def _get_human_users(user_list: Iterable[User]) -> Iterable[User]:
        return [user for user in user_list if not user.is_bot]
