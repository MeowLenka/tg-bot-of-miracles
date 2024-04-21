import os
import pprint
import random

import requests
from dotenv import load_dotenv

from opentdb import all_opentdb_categories

load_dotenv()
BOT_TOKEN = os.getenv('TG_TOKEN')
PROGRAM_API_TOKEN = os.getenv('PROGRAM_API_TOKEN')

dif_dict = {
    'Простой': 'easy', 'Средний': 'medium', 'Сложный': 'hard'
}

categories_dict = {
    'Наука': {
        'Математика': 'Science: Mathematics',
        'Информатика': 'Science: Computers',
        'История': 'History',
        'География': 'Geography',
        'Окружающий мир': 'Science & Nature'
    },
    'Искусство': {
        'Театр': 'Entertainment: Musicals & Theatres',
        'Кино': 'Entertainment: Film',
        'Музыка': 'Entertainment: Music',
        'Живопись': 'Art'
    },
    'Спорт': 'Sports',
    'Игры': {
        'Компьютерные': 'Entertainment: Video Games',
        'Настольные': 'Entertainment: Board Games'
    },
    'Еда': 'food',
    'Общие знания': 'General Knowledge'
}


def get_json_quizapi(group, dif, tag, lim):
    request = (f'https://quizapi.io/api/v1/questions?apiKey={PROGRAM_API_TOKEN}'
               f'&category={group}&difficulty={dif}&limit={lim}')
    response = requests.get(request, headers={"User-Agent": ""})
    return response.json()


def get_json_opentdb(group, dif, kind, lim):
    request = (f'https://opentdb.com/api.php?amount={lim}&'
               f'category={all_opentdb_categories[group]}&difficulty={dif}&type={kind}')
    response = requests.get(request)
    return response.json()


def get_response_triviaapi():
    request = f'https://the-trivia-api.com/v2/questions'
    request = 'https://opentdb.com/api..php&apikey='


if __name__ == '__main__':
    print('Выберите категорию: 1. вопросы из QuizAPI 2. вопросы из Trivia API 3. вопросы из the-trivia-api')
    category = int(input())
    if category == 1:
        group = random.choice(['CMS', 'Code', 'DevOps', 'Docker',
                               'Linux', 'SQL', 'bash', 'uncategorized'])
        difficulty = random.choice(['easy', 'medium', 'hard'])
        tag = random.choice(['Git', 'MySQL', 'Python'])
        limit = 5
        questions = get_json_quizapi(group, difficulty, tag, limit)
        for quest in questions:
            if quest['correct_answer']:
                print(quest['question'])
                for let, ans in quest['answers'].items():
                    if ans:
                        print(let[-1], ans)
                # print('correct_answer: ', quest['correct_answer'][-1])
                print('-------------------')
                user_answer = input()
                print(quest['correct_answer'][-1])
                if user_answer == quest['correct_answer'][-1]:
                    print('Правильно!')
                else:
                    print('Неверно. Правильный ответ: ', quest['correct_answer'][-1])
                    if quest['explanation']:
                        print(quest['explanation'])

    elif category == 2:
        group = random.choice(['General Knowledge',
                               'Entertainment: Books',
                               'Entertainment: Film',
                               'Entertainment: Music',
                               'Entertainment: Video Games',
                               'Science & Nature',
                               'Science: Mathematics',
                               'Sports',
                               'Geography',
                               'History',
                               'Art'])
        difficulty = random.choice(['easy', 'medium', 'hard'])
        kind = random.choice(['multiple', 'boolean'])
        limit = 5
        questions = get_json_opentdb(group, difficulty, kind, limit)
        for quest in questions['results']:
            letters = 'abcdefghigkl'
            print(quest['question'])
            answers = quest['incorrect_answers']
            answers.append(quest['correct_answer'])
            random.shuffle(answers)
            variants = {}
            for n, a in enumerate(answers):
                variants[letters[n]] = a
                print(letters[n], a)
            print('-------------------')
            user_answer = input()
            if variants[user_answer] == quest['correct_answer']:
                print('Правильно!')
            else:
                print('Неверно. Правильный ответ: ', quest['correct_answer'])

    elif category == 3:
        pass
