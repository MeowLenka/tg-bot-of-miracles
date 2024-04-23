import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, filters, CommandHandler, CallbackContext, MessageHandler, ConversationHandler

import quizapi
import triviaapi
import opentdb

from support import *
from database import DataBase

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

db = DataBase('database_info.db')
translator = GoogleTranslator(source='auto', target='ru')


async def on_stop(update, context: CallbackContext):
    await update.message.reply_text(text='Пока! Надеюсь, мы с тобой еще пообщаемся', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


async def on_start(update, context: CallbackContext):
    keyboard = ReplyKeyboardMarkup([['/begin']])
    await update.message.reply_text(text='Привет! Хочешь проверить свой кругозор, узнать что-то новое и '

                                         'сразиться с другими? Тогда давай начнем!', reply_markup=keyboard)


async def on_begin(update, context: CallbackContext):
    main_keyboard = ReplyKeyboardMarkup(main_markup)
    user_id = context._user_id
    if not db.user_exists(user_id):
        db.add_user(user_id)
    await update.message.reply_text(text='Добро пожаловать', reply_markup=main_keyboard)
    return 1


async def choose_category(update, context: CallbackContext):
    text = update.message.text
    if text == 'Подборка викторин':
        quizzes_keyboard = ReplyKeyboardMarkup(quizzes_selection_markup)
        await update.message.reply_text(text='Выберите категорию', reply_markup=quizzes_keyboard)
        return 2
    if text == 'Личный кабинет':
        account_keyboard = ReplyKeyboardMarkup(pers_account_markup)
        await update.message.reply_text(text='Личный кабинет:', reply_markup=account_keyboard)
        return 102
    # elif text == 'Скрыть':
    #     await update.message.reply_text(text='Клавиатура скрыта', reply_markup=ReplyKeyboardRemove())
    # elif text == 'Назад':
    #     return ConversationHandler.END


async def choose_difficulty_level(update, context: CallbackContext):
    category = update.message.text
    if category == 'Назад':
        main_keyboard = ReplyKeyboardMarkup(main_markup)
        await update.message.reply_text(text='Давай начнем!', reply_markup=main_keyboard)
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
    context.user_data['kind'] = kind

    await update.message.reply_text(text='Давайте начнем!', reply_markup=ReplyKeyboardMarkup([['Ок!']]))
    return 5


async def quiz_ask_question(update, context: CallbackContext):
    category = context.user_data['category']
    difficulty = dif_dict[context.user_data['difficulty']]
    limit = 1
    if category == 'Программирование':
        group = context.user_data['kind']
        json = quizapi.get_json_quizapi(group, difficulty, limit)
    elif category == 'Общие знания':
        json = triviaapi.get_json_triviaapi()
    else:
        if context.user_data['kind']:
            group = categories_dict[category][context.user_data['kind']]
        else:
            group = categories_dict[category]
        kind = random.choice(['multiple', 'boolean'])
        json = opentdb.get_json_opentdb(group, difficulty, kind, limit)

    if json:
        quest, answ = opentdb.get_qa_opentdb(json)
        context.user_data['current_question'] = quest
        context.user_data['num_of_quest'] += 1
        answers_keyboard = ReplyKeyboardMarkup(answ)
        await update.message.reply_text(text=f"{context.user_data['num_of_quest']}. "
                                             f"{quest}", reply_markup=answers_keyboard)
        return 6


async def quiz_check_answer(update, context: CallbackContext):
    user_answer = update.message.text
    quest = context.user_data['current_question']
    category = context.user_data['category']

    db.update_count(context._user_id, 1, 'count_of_all_answers')

    if category == 'Программирование':
        correct = translator.translate(text=quest['answers'][quest['correct_answer']])
        if user_answer == correct:
            text = 'Правильно!'
            context.user_data['num_of_cor_answ'] += 1
            db.update_count(context._user_id, 1, 'count_of_cor_answers')
        else:
            if quest['explanation']:
                text = (f"Неверно.\n"
                        f"Правильный ответ: {correct} \n"
                        f"Пояснение: {quest['explanation']}")
            else:
                text = (f"Неверно.\n"
                        f"Правильный ответ: {correct}")

    elif category == 'Общие знания':
        correct = translator.translate(quest['correctAnswer'])
        if user_answer == correct:
            context.user_data['num_of_cor_answ'] += 1
            text = 'Правильно!'
            db.update_count(context._user_id, 1, 'count_of_cor_answers')
        else:
            text = (f"Неверно.\n"
                    f"Правильный ответ: {correct}")
    else:
        correct = translator.translate(quest['correct_answer'])
        if user_answer == correct:
            context.user_data['num_of_cor_answ'] += 1
            text = 'Правильно!'
            db.update_count(context._user_id, 1, 'count_of_cor_answers')
        else:
            text = (f"Неверно.\n"
                    f"Правильный ответ: {correct}")

    num = 5 - context.user_data['num_of_quest']
    if num > 0:
        await update.message.reply_text(text=text,
                                        reply_markup=ReplyKeyboardMarkup([['Дальше']]))
        return 5
    else:
        await update.message.reply_text(text=f"{text}\n\nЭто был последний вопрос",
                                        reply_markup=ReplyKeyboardMarkup([['Результаты']]))
        return 7


async def show_the_results(update, context: CallbackContext):
    db.update_count(context._user_id, 1, 'count_of_quizes')

    keyboard = ReplyKeyboardMarkup([['Подборка викторин', 'Личный кабинет'], ['Скрыть']])
    text = (f"Ваш результат: \n"
            f"Верно - {context.user_data['num_of_cor_answ']} \n"
            f"Неверно - {5 - context.user_data['num_of_cor_answ']}")
    await update.message.reply_text(text=text, reply_markup=keyboard)
    return 1


async def see_account(update, context: CallbackContext):
    choose = update.message.text
    if choose == 'Назад':
        main_keyboard = ReplyKeyboardMarkup(main_markup)
        await update.message.reply_text(text='Давай начнем!', reply_markup=main_keyboard)
        return 1
    if choose == 'Посмотреть статистику':
        quizzes = db.get_count(context._user_id, 'count_of_quizes')
        all_answers = db.get_count(context._user_id, 'count_of_all_answers')
        cor_answers = db.get_count(context._user_id, 'count_of_cor_answers')
        text = (f'Ваша статистика:\n'
                f'\nКоличество пройденных викторин: {quizzes}'
                f'\nКоличество всех ответов: {all_answers}'
                f'\nКоличество правильных ответов: {cor_answers} \n'
                f'\nПроцент правильных ответов: {int((cor_answers / all_answers) * 100)}%')
        await update.message.reply_text(text=text, reply_markup=ReplyKeyboardMarkup([['Назад']]))


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    start_handler = CommandHandler('start', on_start)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('begin', on_begin)],
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
    application.add_handler(start_handler)
    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
