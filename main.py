import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, filters, CommandHandler, CallbackContext, MessageHandler, ConversationHandler

from work_with_api import *

load_dotenv()
BOT_TOKEN = os.getenv('TG_TOKEN')
API_TOKEN = os.getenv('PROGRAM_API_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

quizzes_selection = [['Программирование', 'Наука'], ['Спорт', 'Игры'],
                     ['Искусство', 'Еда'], ['Общие знания']]
difficulty_selection = [['Простой', 'Средний', 'Сложный'], ['Случайный']]


async def on_stop(update, context: CallbackContext):
    await update.message.reply_text(text='Пока! Надеюсь, мы с тобой еще пообщаемся', reply_markup=ReplyKeyboardRemove())


async def on_start(update, context: CallbackContext):
    keyboard = ReplyKeyboardMarkup([['Подборка викторин', 'Личный кабинет'], ['Скрыть']])
    await update.message.reply_text(text='Привет! Хочешь проверить свой кругозор, узнать что-то новое и '

                                         'сразиться с другими? Тогда давай начнем!', reply_markup=keyboard)
    return 1


async def choose_category(update, context: CallbackContext):
    text = update.message.text
    if text == 'Подборка викторин':
        quizzes_keyboard = ReplyKeyboardMarkup([*quizzes_selection, ['Назад']])
        await update.message.reply_text(text='Выберите категорию', reply_markup=quizzes_keyboard)
        return 2
    elif text == 'Скрыть':
        await update.message.reply_text(text='Клавиатура скрыта', reply_markup=ReplyKeyboardRemove())
    elif text == 'Назад':
        await on_start(update, context)


async def choose_difficulty_level(update, context: CallbackContext):
    category = update.message.text
    if category == 'Назад':
        keyboard = ReplyKeyboardMarkup([['Подборка викторин', 'Личный кабинет'], ['Скрыть']])
        await update.message.reply_text(text='Давай начнем!', reply_markup=keyboard)
        return 1
    context.user_data['category'] = category
    difficulty_keyboard = ReplyKeyboardMarkup([*difficulty_selection, ['Назад']])
    await update.message.reply_text(text='Выберите уровень сложности', reply_markup=difficulty_keyboard)
    return 3


async def choose_quize_kind(update, context: CallbackContext):
    difficulty = update.message.text
    context.user_data['difficulty'] = difficulty
    if difficulty == 'Назад':
        quizzes_keyboard = ReplyKeyboardMarkup([*quizzes_selection, ['Назад']])
        await update.message.reply_text(text='Выберите категорию', reply_markup=quizzes_keyboard)
        return 2
    category = context.user_data['category']
    if category == 'Программирование':
        kinds_keyboard = ReplyKeyboardMarkup([['CMS', 'Code'], ['DevOps', 'Docker'],
                                              ['Linux', 'SQL'], ['bash', 'uncategorized'],
                                              ['Случайное'], ['Назад']])
        await update.message.reply_text(text='Выберите направление', reply_markup=kinds_keyboard)
    elif category == 'Наука':
        kinds_keyboard = ReplyKeyboardMarkup([['Математика'], ['Информатика'], ['История'], ['География'],
                                              ['Окружающий мир'], ['Случайное'], ['Назад']])
        await update.message.reply_text(text='Выберите направление', reply_markup=kinds_keyboard)
    elif category == 'Игры':
        kinds_keyboard = ReplyKeyboardMarkup([['Компьютерные'], ['Настольные'], ['Случайное'], ['Назад']])
        await update.message.reply_text(text='Выберите направление', reply_markup=kinds_keyboard)
    elif category == 'Искусство':
        kinds_keyboard = ReplyKeyboardMarkup([['Театр', 'Кино'], ['Музыка', 'Живопись'], ['Случайное'], ['Назад']])
        await update.message.reply_text(text='Выберите направление', reply_markup=kinds_keyboard)
    else:
        return 5
    return 4


async def quiz_pre_start(update, context: CallbackContext):
    kind = update.message.text
    if kind == 'Назад':
        quizzes_keyboard = ReplyKeyboardMarkup([*quizzes_selection, ['Назад']])
        await update.message.reply_text(text='Выберите категорию', reply_markup=quizzes_keyboard)
        return 2
    context.user_data['kind'] = kind
    ok_keyboard = ReplyKeyboardMarkup([['Ок!']])
    await update.message.reply_text(text='Давайте начнем!', reply_markup=ok_keyboard)
    return 5


async def quiz_start(update, context: CallbackContext):
    category = context.user_data['category']
    difficulty = dif_dict[context.user_data['difficulty']]
    limit = 1
    if category == 'Программирование':
        group = context.user_data['kind']
        tag = random.choice(['Git', 'MySQL', 'Python'])
        questions = get_json_quizapi(group, difficulty, tag, limit)
        for quest in questions:
            if quest['correct_answer']:
                answ = []
                for let, ans in quest['answers'].items():
                    if ans:
                        answ.append([f'{let[-1]}. {ans}'])
                answers_keyboard = ReplyKeyboardMarkup(answ)
                await update.message.reply_text(text=quest['question'], reply_markup=answers_keyboard)

    if category == 'Еда':
        pass
    else:
        if context.user_data['kind']:
            group = categories_dict[category][context.user_data['kind']]
        else:
            group = categories_dict[category]
        print(group)
        kind = random.choice(['multiple', 'boolean'])
        questions = get_json_opentdb(group, difficulty, kind, limit)
        # letters = 'abcdefghigkl'
        for quest in questions['results']:
            answ = quest['incorrect_answers']
            answ.append(quest['correct_answer'])
            random.shuffle(answ)
            answers_keyboard = ReplyKeyboardMarkup([answ])
            await update.message.reply_text(text=quest['question'], reply_markup=answers_keyboard)

    # await update.message.reply_text(text='Тут жесткая викторина!')


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', on_start)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_category)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_difficulty_level)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_quize_kind)],
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, quiz_pre_start)],
            5: [MessageHandler(filters.TEXT & ~filters.COMMAND, quiz_start)]
        },
        fallbacks=[CommandHandler('stop', on_stop)]
    )
    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
