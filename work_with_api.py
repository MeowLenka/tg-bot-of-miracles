import os
import random

import requests
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('TG_TOKEN')
PROGRAM_API_TOKEN = os.getenv('PROGRAM_API_TOKEN')


def get_response_quiz():
    request = 'https://opentdb.com/api.php?amount=10&category=9&difficulty=medium&type=multiple'
    response = requests.get(request)
    return response


def get_json_quizapi(group, dif, tag, lim):
    request = (f'https://quizapi.io/api/v1/questions?apiKey={PROGRAM_API_TOKEN}'
               f'&category={group}&difficulty={dif}&limit={lim}')
    response = requests.get(request, headers={"User-Agent": ""})
    return response.json()


def get_response_quiz_de():
    request = f'https://opentdb.com/api..php&apikey={PROGRAM_API_TOKEN} '


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
                if user_answer == quest['correct_answer'][-1]:
                    print('Правильно!')
                else:
                    print('Неверно. Правильный ответ: ', quest['correct_answer'][-1])
                    if quest['explanation']:
                        print(quest['explanation'])

    elif category == 2:
        group = []
        difficulty = []
        kind = ''
        limit = 5
    elif category == 3:
        pass
