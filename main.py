import logging
import os
import requests

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, filters, CommandHandler, CallbackContext, MessageHandler
from dotenv import load_dotenv

from work_with_api import *

load_dotenv()
BOT_TOKEN = os.getenv('TG_TOKEN')
API_TOKEN = os.getenv('PROGRAM_API_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def on_stop(update, context: CallbackContext):
    await update.message.reply_text(text='Пока! Надеюсь, мы с тобой еще пообщаемся', reply_markup=ReplyKeyboardRemove())


async def on_start(update, context: CallbackContext):
    keyboard = ReplyKeyboardMarkup([['Подборка викторин', 'Личный кабинет'], ['Скрыть']])
    await update.message.reply_text(text='Привет! Хочешь проверить свой кругозор, узнать что-то новое и '
                                         'сразиться с другими? Тогда давай начнем!', reply_markup=keyboard)


async def on_message(update, context: CallbackContext):
    text = update.message.text
    if text == 'Подборка викторин':
        quizzes_keyboard = ReplyKeyboardMarkup([['Программирование', 'История', 'Искусство', 'Видеоигры'], ['Назад']])
        await update.message.reply_text(text='Выберите категорию', reply_markup=quizzes_keyboard)
    elif text == 'Скрыть':
        await update.message.reply_text(text='Клавиатура скрыта', reply_markup=ReplyKeyboardRemove())
    elif text == 'Назад':
        await on_start(update, context)


async def on_quize(update, context: CallbackContext):
    text = update.message.text
    if text == '':
        pass


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", on_start))
    application.add_handler(CommandHandler("stop", on_stop))
    application.add_handler(MessageHandler(filters=filters.TEXT & ~filters.COMMAND, callback=on_message))
    application.run_polling()


if __name__ == '__main__':
    main()
