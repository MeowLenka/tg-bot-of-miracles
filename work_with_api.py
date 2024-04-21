import random
import requests


from opentdb import all_opentdb_categories
from support import PROGRAM_API_TOKEN


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


def get_json_triviaapi():
    request = f'https://the-trivia-api.com/v2/questions'
    response = requests.get(request, headers={"User-Agent": ""})
    return response.json()


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
        questions = get_json_opentdb('General Knowledge', difficulty, kind, limit)
        print(questions)
        # for quest in questions['results']:
        #     letters = 'abcdefghigkl'
        #     print(quest['question'])
        #     answers = quest['incorrect_answers']
        #     answers.append(quest['correct_answer'])
        #     random.shuffle(answers)
        #     variants = {}
        #     for n, a in enumerate(answers):
        #         variants[letters[n]] = a
        #         print(letters[n], a)
        #     print('-------------------')
        #     user_answer = input()
        #     print(quest['correct_answer'])
        #     if variants[user_answer] == quest['correct_answer']:
        #         print('Правильно!')
        #     else:
        #         print('Неверно. Правильный ответ: ', quest['correct_answer'])

    elif category == 3:
        pass
