import logging
from typing import NoReturn, Iterable, Dict, List

from telegram import Bot, Update, User, Message
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, Dispatcher, CallbackContext

import pictureresponsebot.config as config
from pictureresponsebot.util import call_and_log, bot_send_picture

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

TelegramMessageArgs = Dict[str, Bot or int or str]


class PictureResponseBot:

    def __init__(self, token: str) -> NoReturn:
        self.token: str = token

    def run(self) -> NoReturn:
        updater: Updater = Updater(self.token, use_context=True)
        dp: Dispatcher = updater.dispatcher
        dp.add_handler(CommandHandler(config.COMMAND_NAME, self._send_picture_from_command))
        dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, self._respond_to_new_members))
        updater.start_polling()
        logging.info("bot is running")
        updater.idle()

    @bot_send_picture
    @call_and_log
    def _respond_to_new_members(self, update: Update, context: CallbackContext) -> TelegramMessageArgs:
        return self._construct_message_object(context.bot, update.message.chat.id, self._get_welcome_message(update.message))

    @bot_send_picture
    @call_and_log
    def _send_picture_from_command(self, update: Update, context: CallbackContext) -> TelegramMessageArgs:
        return self._construct_message_object(context.bot, update.message.chat.id, config.COMMAND_REPLY, update.message.message_id)

    def _construct_message_object(self, from_bot: Bot, chat_id: int, caption: str, reply_id: int = None) -> TelegramMessageArgs:
        return {'self': from_bot,
                'chat_id': chat_id,
                'caption': caption,
                'reply_id': reply_id}

    def _get_welcome_message(self, message: Message) -> str:
        human_users: List[User] = self._get_human_users(message.new_chat_members)
        response_text: str = ", ".join([user.name for user in human_users])
        welcome_chat: str = config.NEW_USER_REPLY.format(new_member_names=response_text,
                                                         chat_name=message.chat.title)
        return welcome_chat

    def _get_human_users(self, user_list: Iterable[User]) -> List[User]:
        return [user for user in user_list if not user.is_bot]
