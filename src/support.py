import os
import random

from dotenv import load_dotenv
from deep_translator import GoogleTranslator

load_dotenv()
BOT_TOKEN = os.getenv('TG_TOKEN')
PROGRAM_API_TOKEN = os.getenv('PROGRAM_API_TOKEN')
translator = GoogleTranslator(source='auto', target='ru')

dif_dict = {
    'Простой': 'easy', 'Средний': 'medium', 'Сложный': 'hard',
    'Случайный': random.choice(['easy', 'medium', 'hard'])
}

categories_dict = {
    'Программирование': {
        'CMS': 'CMS',
        'Кодинг': 'Code',
        'DevOps': 'DevOps',
        'Docker': 'Docker',
        'Linux': 'Linux',
        'SQL': 'SQL',
        'bash': 'bash',
        'Без категории': 'uncategorized',
        'Случайное': random.choice(['CMS', 'Code', 'DevOps', 'Docker',
                                    'Linux', 'SQL', 'bash', 'uncategorized'])
    },
    'Наука': {
        'Математика': 'Science: Mathematics',
        'Информатика': 'Science: Computers',
        'История': 'History',
        'География': 'Geography',
        'Окружающий мир': 'Science & Nature',
        'Случайное': random.choice(['Science: Mathematics', 'Science: Computers',
                                    'History', 'Geography', 'Science & Nature'])
    },
    'Искусство': {
        'Театр': 'Entertainment: Musicals & Theatres',
        'Кино': 'Entertainment: Film',
        'Музыка': 'Entertainment: Music',
        'Живопись': 'Art',
        'Случайное': random.choice(['Entertainment: Musicals & Theatres', 'Entertainment: Film',
                                    'Entertainment: Music', 'Art'])
    },
    'Спорт': 'Sports',
    'Игры': {
        'Компьютерные': 'Entertainment: Video Games',
        'Настольные': 'Entertainment: Board Games',
        'Случайное': random.choice(['Entertainment: Video Games', 'Entertainment: Board Games'])
    },
    'Общие знания': 'General Knowledge'
}

main_markup = [['Подборка викторин', 'Личный кабинет'], ['/stop']]

pers_account_markup = [['Посмотреть статистику', 'Мои викторины'], ['Назад']]

programming_kinds_markup = [['CMS', 'Кодинг'], ['DevOps', 'Docker'],
                            ['Linux', 'SQL'], ['bash', 'Без категории'],
                            ['Случайное'], ['Назад']]

science_kinds_markup = [['Математика'], ['Информатика'], ['История'], ['География'],
                        ['Окружающий мир'], ['Случайное'], ['Назад']]

game_kinds_markup = [['Компьютерные'], ['Настольные'], ['Случайное'], ['Назад']]

art_kinds_markup = [['Театр', 'Кино'], ['Музыка', 'Живопись'], ['Случайное'], ['Назад']]

quizzes_selection_markup = [['Программирование', 'Наука'], ['Спорт', 'Игры'],
                            ['Искусство'], ['Общие знания'], ['Назад']]

difficulty_selection_markup = [['Простой', 'Средний', 'Сложный'], ['Случайный'], ['Назад']]
