import logging
from typing import Dict
from typing import Iterable
from typing import List
from typing import NoReturn

from telegram import Bot
from telegram import Message
from telegram import Update
from telegram import User
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import Dispatcher
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater

from pictureresponsebot.util import bot_send_picture
from pictureresponsebot.util import call_and_log

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

TelegramMessageArgs = Dict[str, Bot or int or str or bytes]


class PictureResponseBot:

    def __init__(self, *args, **kwargs) -> NoReturn:
        try:
            self.token = kwargs["bot_token"]
            self.new_user_reply = kwargs["new_user_reply"]
            self.command_name = kwargs["command_name"]
            self.command_reply = kwargs["command_reply"]
            image_directory = kwargs["image_directory"]
            image_name = kwargs["image_name"]
            self.image_path = "".join([image_directory, image_name])
        except KeyError:
            print("Malformed config file")
        except FileNotFoundError:
            print("Image not found")
        else:
            self.run()

    def run(self) -> NoReturn:
        updater: Updater = Updater(self.token, use_context=True)
        dp: Dispatcher = updater.dispatcher
        dp.add_handler(CommandHandler(self.command_name, self._send_picture_from_command))
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
        return self._construct_message_object(context.bot, update.message.chat.id, self.command_reply, update.message.message_id)

    def _construct_message_object(self, from_bot: Bot, chat_id: int, caption: str, reply_id: int = None) -> TelegramMessageArgs:
        return {'self': from_bot,
                'chat_id': chat_id,
                'caption': caption,
                'reply_id': reply_id,
                'image_path': self.image_path}

    def _get_welcome_message(self, message: Message) -> str:
        human_users: List[User] = self._get_human_users(message.new_chat_members)
        response_text: str = ", ".join([user.name for user in human_users])
        welcome_chat: str = self.new_user_reply.format(new_member_names=response_text,
                                                       chat_name=message.chat.title)
        return welcome_chat

    def _get_human_users(self, user_list: Iterable[User]) -> List[User]:
        return [user for user in user_list if not user.is_bot]
