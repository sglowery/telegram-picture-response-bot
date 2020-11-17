import logging
import os
from typing import Iterable
from typing import List
from typing import NoReturn
from typing import Optional

from telegram import Bot
from telegram import Message
from telegram import Update
from telegram import User
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater

from pictureresponsebot.TelegramMessageArgs import TelegramMessageArgs
from pictureresponsebot.util import bot_send_picture
from pictureresponsebot.util import call_and_log

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


class PictureResponseBot:

    def __init__(self) -> NoReturn:
        self.token = os.environ.get("TELEGRAM_BOT_TOKEN")
        self.new_user_reply = os.environ.get("NEW_USER_REPLY")
        self.command_name = os.environ.get("COMMAND_NAME")
        self.command_reply = os.environ.get("COMMAND_REPLY")
        self.heroku_app_name = os.environ.get("HEROKU_APP_NAME")
        if not self.token or not self.new_user_reply or not self.command_name or not self.command_reply or not self.heroku_app_name:
            logger.error("environment variables missing")
        else:
            logger.info("environment variables set")
            self.run()

    def run(self):
        updater = Updater(self.token, use_context=True)
        dp = updater.dispatcher
        dp.add_handler(CommandHandler(self.command_name, self._send_picture_from_command))
        dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, self._respond_to_new_members))
        port = int(os.environ.get('PORT', '5000'))
        updater.start_webhook(listen="0.0.0.0",
                              port=port,
                              url_path=self.token)
        updater.bot.setWebhook(f"https://{self.heroku_app_name}.herokuapp.com/{self.token}")
        logging.info("bot is running")
        updater.idle()

    @bot_send_picture
    @call_and_log
    def _respond_to_new_members(self, update: Update, context: CallbackContext) -> Optional[TelegramMessageArgs]:
        message: str = self._get_welcome_message(update.message)
        if message:
            return self._construct_message_object(context.bot,
                                                  update.message.chat.id,
                                                  self._get_welcome_message(update.message))
        return None

    @bot_send_picture
    @call_and_log
    def _send_picture_from_command(self, update: Update, context: CallbackContext) -> TelegramMessageArgs:
        return self._construct_message_object(context.bot,
                                              update.message.chat.id,
                                              self.command_reply,
                                              update.message.message_id)

    def _construct_message_object(self,
                                  from_bot: Bot,
                                  chat_id: int,
                                  caption: str,
                                  reply_id: int = None) -> TelegramMessageArgs:
        return {'self':       from_bot,
                'chat_id':    chat_id,
                'caption':    caption,
                'reply_id':   reply_id,
                'image_path': self.image_path}

    def _get_welcome_message(self, message: Message) -> Optional[str]:
        human_users: List[User] = self._get_human_users(message.new_chat_members)
        if len(human_users) > 0:
            response_text = ", ".join(user.name for user in human_users)
            welcome_chat = self.new_user_reply.format(new_member_names=response_text,
                                                      chat_name=message.chat.title)
            return welcome_chat
        return None

    def _get_human_users(self, user_list: Iterable[User]) -> List[User]:
        return [user for user in user_list if not user.is_bot]
