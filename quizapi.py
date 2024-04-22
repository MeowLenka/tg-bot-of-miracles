import random
import requests

from opentdb import all_opentdb_categories
from support import PROGRAM_API_TOKEN

all_quizapi_categories = ['CMS', 'Code', 'DevOps', 'Docker',
                          'Linux', 'SQL', 'bash', 'uncategorized']

all_quizapi_tags = ['.Net', 'AI', 'AWS', 'Angular', 'BASH',
                    'Blockchain', 'C', 'Css', 'DevOps', 'Docker',
                    'Git', 'HTML', 'Java', 'JavaScript', 'Kubernetes',
                    'Laravel', 'Linux', 'MySQL', 'Node.js', 'PHP',
                    'Python', 'React', 'Ruby', 'Swift', 'Undefined',
                    'VsCode', 'VueJS', 'WordPress', 'dev', 'postgres']


class QuizApi:
    def get_json(self, group, dif, lim):
        request = (f'https://quizapi.io/api/v1/questions?apiKey={PROGRAM_API_TOKEN}'
                   f'&category={group}&difficulty={dif}&limit={lim}')
        response = requests.get(request, headers={"User-Agent": ""})
        return response.json()

    def get_question_and_answers(self, questions: list):
        for quest in questions:
            if quest['correct_answer']:
                answ = []
                for let, ans in quest['answers'].items():
                    if ans:
                        answ.append([ans])
            return quest, answ

