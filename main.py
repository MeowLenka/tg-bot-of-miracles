import logging
import random

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, filters, CommandHandler, CallbackContext, MessageHandler, ConversationHandler

from work_with_api import get_json_quizapi, get_json_opentdb, get_json_triviaapi
from support import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


async def on_stop(update, context: CallbackContext):
    await update.message.reply_text(text='Пока! Надеюсь, мы с тобой еще пообщаемся', reply_markup=ReplyKeyboardRemove())


async def on_start(update, context: CallbackContext):
    keyboard = ReplyKeyboardMarkup(main_markup)
    await update.message.reply_text(text='Привет! Хочешь проверить свой кругозор, узнать что-то новое и '

                                         'сразиться с другими? Тогда давай начнем!', reply_markup=keyboard)
    return 1


async def choose_category(update, context: CallbackContext):
    text = update.message.text
    if text == 'Подборка викторин':
        quizzes_keyboard = ReplyKeyboardMarkup(quizzes_selection_markup)
        await update.message.reply_text(text='Выберите категорию', reply_markup=quizzes_keyboard)
        return 2
    if text == 'Личный кабинет':
        quizzes_keyboard = ReplyKeyboardMarkup(quizzes_selection_markup)
        await update.message.reply_text(text='Личный кабинет:', reply_markup=quizzes_keyboard)
        return 102
    elif text == 'Скрыть':
        await update.message.reply_text(text='Клавиатура скрыта', reply_markup=ReplyKeyboardRemove())
    elif text == 'Назад':
        await on_start(update, context)


async def choose_difficulty_level(update, context: CallbackContext):
    category = update.message.text
    if category == 'Назад':
        keyboard = ReplyKeyboardMarkup(main_markup)
        await update.message.reply_text(text='Давай начнем!', reply_markup=keyboard)
        return 1
    context.user_data['category'] = category
    difficulty_keyboard = ReplyKeyboardMarkup(difficulty_selection_markup)
    await update.message.reply_text(text='Выберите уровень сложности', reply_markup=difficulty_keyboard)
    return 3


async def choose_quize_kind(update, context: CallbackContext):
    difficulty = update.message.text
    context.user_data['difficulty'] = difficulty
    if difficulty == 'Назад':
        quizzes_keyboard = ReplyKeyboardMarkup(quizzes_selection_markup)
        await update.message.reply_text(text='Выберите категорию', reply_markup=quizzes_keyboard)
        return 2
    category = context.user_data['category']
    context.user_data['num_of_quest'] = 0
    context.user_data['num_of_cor_answ'] = 0
    context.user_data['kind'] = None
    if category == 'Программирование':
        kinds_keyboard = ReplyKeyboardMarkup(programming_kinds_markup)
        await update.message.reply_text(text='Выберите направление', reply_markup=kinds_keyboard)
    elif category == 'Наука':
        kinds_keyboard = ReplyKeyboardMarkup(science_kinds_markup)
        await update.message.reply_text(text='Выберите направление', reply_markup=kinds_keyboard)
    elif category == 'Игры':
        kinds_keyboard = ReplyKeyboardMarkup(game_kinds_markup)
        await update.message.reply_text(text='Выберите направление', reply_markup=kinds_keyboard)
    elif category == 'Искусство':
        kinds_keyboard = ReplyKeyboardMarkup(art_kinds_markup)
        await update.message.reply_text(text='Выберите направление', reply_markup=kinds_keyboard)
    else:
        return 5
    return 4


async def quiz_pre_start(update, context: CallbackContext):
    kind = update.message.text
    if kind == 'Назад':
        quizzes_keyboard = ReplyKeyboardMarkup(quizzes_selection_markup)
        await update.message.reply_text(text='Выберите категорию', reply_markup=quizzes_keyboard)
        return 2
    # context.user_data['num_of_quest'] = 0
    # context.user_data['num_of_cor_answ'] = 0
    context.user_data['kind'] = kind

    await update.message.reply_text(text='Давайте начнем!', reply_markup=ReplyKeyboardMarkup([['Ок!']]))
    return 5


async def quiz_ask_question(update, context: CallbackContext):
    category = context.user_data['category']
    difficulty = dif_dict[context.user_data['difficulty']]
    limit = 1
    if category == 'Программирование':
        group = context.user_data['kind']
        tag = random.choice(['Git', 'MySQL', 'Python'])
        questions = get_json_quizapi(group, difficulty, tag, limit)
        for quest in questions:
            if quest['correct_answer']:
                context.user_data['current_question'] = quest
                answ = []
                for let, ans in quest['answers'].items():
                    if ans:
                        answ.append([f'{let[-1]}. {ans}'])
                answers_keyboard = ReplyKeyboardMarkup(answ)
                await update.message.reply_text(text=quest['question'], reply_markup=answers_keyboard)
                context.user_data['num_of_quest'] += 1
                return 6
    elif category == 'Общие знания':
        group = categories_dict[category]
        questions = get_json_triviaapi()
        for quest in questions:
            if quest['difficulty'] == difficulty:
                context.user_data['current_question'] = quest
                answ = quest['incorrectAnswers']
                answ.append(quest['correctAnswer'])
                random.shuffle(answ)
                answers_keyboard = ReplyKeyboardMarkup([answ])
                await update.message.reply_text(text=quest['question']['text'], reply_markup=answers_keyboard)
                context.user_data['num_of_quest'] += 1
                return 6
    else:
        if context.user_data['kind']:
            group = categories_dict[category][context.user_data['kind']]
        else:
            group = categories_dict[category]
        kind = random.choice(['multiple', 'boolean'])
        questions = get_json_opentdb(group, difficulty, kind, limit)
        # letters = 'abcdefghigkl'
        for quest in questions['results']:
            context.user_data['current_question'] = quest
            answ = quest['incorrect_answers']
            answ.append(quest['correct_answer'])
            random.shuffle(answ)
            answers_keyboard = ReplyKeyboardMarkup([answ])
            await update.message.reply_text(text=quest['question'], reply_markup=answers_keyboard)
            context.user_data['num_of_quest'] += 1
            return 6

    # await update.message.reply_text(text='Тут жесткая викторина!')


async def quiz_check_answer(update, context: CallbackContext):
    user_answer = update.message.text
    quest = context.user_data['current_question']
    category = context.user_data['category']

    if category == 'Программирование':
        if user_answer[0] == quest['correct_answer'][-1]:
            # text = 'Правильно!'
            context.user_data['num_of_cor_answ'] += 1
    elif category == 'Общие знания':
        if user_answer == quest['correctAnswer']:
            context.user_data['num_of_cor_answ'] += 1
        # else:
        #     text = f"Неверно. Правильный ответ: {quest['correct_answer'][-1]}"
    else:
        if user_answer == quest['correct_answer']:
            context.user_data['num_of_cor_answ'] += 1

    num = 5 - context.user_data['num_of_quest']
    if num > 0:
        await update.message.reply_text(text=f"Осталось {num} вопрос(а)",
                                        reply_markup=ReplyKeyboardMarkup([['Дальше']]))
        return 5
    else:
        await update.message.reply_text(text=f"Это был последний вопрос",
                                        reply_markup=ReplyKeyboardMarkup([['Результаты']]))
        return 7


async def show_the_results(update, context: CallbackContext):
    keyboard = ReplyKeyboardMarkup([['Подборка викторин', 'Личный кабинет'], ['Скрыть']])
    text = f" Количество правильных ответов: {context.user_data['num_of_cor_answ']}"
    await update.message.reply_text(text=text, reply_markup=keyboard)
    return 1


async def see_account(update, context: CallbackContext):
    keyboard = ReplyKeyboardMarkup([['Подборка викторин', 'Личный кабинет'], ['Скрыть']])
    text = f" Количество правильных ответов: {context.user_data['num_of_cor_answ']}"
    await update.message.reply_text(text=text, reply_markup=keyboard)
    return 1


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', on_start)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_category)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_difficulty_level)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_quize_kind)],
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, quiz_pre_start)],
            5: [MessageHandler(filters.TEXT & ~filters.COMMAND, quiz_ask_question)],
            6: [MessageHandler(filters.TEXT & ~filters.COMMAND, quiz_check_answer)],
            7: [MessageHandler(filters.TEXT & ~filters.COMMAND, show_the_results)],
            102: [MessageHandler(filters.TEXT & ~filters.COMMAND, see_account)],
        },
        fallbacks=[CommandHandler('stop', on_stop)]
    )
    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
