import os
import asyncio
import logging
from dotenv import load_dotenv

from telegram import (
    Update, InputMediaPhoto,
    InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    Application, 
    ContextTypes,
    PicklePersistence,
)
# import handlers
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

load_dotenv(".env")
TELEGRAM_AUTH_TOKEN = os.getenv("TELEGRAM_AUTH_TOKEN")
PATH_TO_IMAGES = "/images"

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

class NotSubscribed(Exception):
    pass
class AlreadySubscribed(Exception):
    pass

def only_files(func):
    def inner(*args, **kwargs):
        if args[1].is_directory:
            return None
        return func(*args, **kwargs)
    return inner
        
class BulkMessaging:
    def __init__(self, application: Application, loop: asyncio.BaseEventLoop):
        self.application = application
        self.loop = loop
    
    def get_subscribed_users(self):
        return self.application.bot_data.get("subscribed_users")
    
    def send(self):
        message = "⚠ Необходимо авторизоваться ⚠"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Получить QR код", callback_data="qrcode")]
        ])
        for chat_id in self.get_subscribed_users():
            self.loop.run_until_complete(self.application.bot.send_message(chat_id, message, reply_markup=keyboard))
                

class EventHandler(FileSystemEventHandler):
    """Logs all the events captured."""
    def __init__(self, bulk: BulkMessaging):
        super().__init__()
        self.bulk = bulk

    @only_files
    def on_created(self, event):
        super().on_created(event)
        logging.info(f"File created {event.src_path}")
        self.bulk.send()
        
    @only_files
    def on_deleted(self, event):
        super().on_deleted(event)

def subsribe_user(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    if not context.bot_data.get("subscribed_users"):
        context.bot_data["subscribed_users"] = set()
    context.bot_data["subscribed_users"].add(chat_id)
    logging.info(f"Subscribed user {chat_id}")
    
def unsubsribe_user(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    if not context.bot_data.get("subscribed_users"):
        context.bot_data["subscribed_users"] = {}
    if chat_id not in context.bot_data["subscribed_users"]:
        raise NotSubscribed
    context.bot_data["subscribed_users"].remove(chat_id)    

async def update_message(text: str, update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.delete()
    message = await context.bot.edit_message_text(text, update.effective_chat.id, context.user_data["message"], parse_mode="HTML")
    context.user_data["message"] = message.id

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "Чтобы подписаться на бота и получать QR код для авторизации в Whatsapp, отправьте команду /subscribe\nЧтобы перестать получать уведомления, отправьте команду /unsubscribe"
    if context.user_data.get("message"):
        try:
            await update_message(message, update, context)
        except:
            await update.effective_message.delete()
            message = await update.effective_chat.send_message(message)
            context.user_data["message"] = message.id
    else:
        await update.effective_message.delete()
        message = await update.effective_chat.send_message(message)
        context.user_data["message"] = message.id

async def subscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    subsribe_user(update.effective_chat.id, context)
    message = "Вы успешно подписались на обновления!\n\n⚠ <b>Закрепите бота в приложении телеграм и не выключайте уведомления. От этого зависит стабильность работы парсера.</b>"
    await update_message(message, update, context)

async def unsubscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        unsubsribe_user(update.effective_chat.id, context)
    except NotSubscribed:
        message = await update_message("Вы еще не подписаны", update, context)
        return
    message = await update_message("Вы успешно отписались от обновлений!", update, context)

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_chat.send_photo("images/qrcode.png")

async def ignore(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.delete()


def get_application():
    """Initialize the bot"""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_AUTH_TOKEN).persistence(PicklePersistence("authbot_persistence.pickle", update_interval=1)).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("subscribe", subscribe_command))
    application.add_handler(CommandHandler("unsubscribe", unsubscribe_command))
    application.add_handler(CallbackQueryHandler(callback_handler))
    application.add_handler(MessageHandler(filters.ALL, ignore))
    
    return application
    

def start_application(application: Application):
    """Start the bot."""
    # Run the bot until the user presses Ctrl-C
    application.run_polling(timeout=30, read_timeout=10)

if __name__ == "__main__":
    application = get_application()
    loop = asyncio.new_event_loop()
    bulk = BulkMessaging(application, loop)
    event_handler = EventHandler(bulk)
    observer = Observer()
    observer.schedule(event_handler, "images")
    observer.start()
    start_application(application)

