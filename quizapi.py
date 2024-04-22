import requests

from support import PROGRAM_API_TOKEN, translator


all_quizapi_categories = ['CMS', 'Code', 'DevOps', 'Docker',
                          'Linux', 'SQL', 'bash', 'uncategorized']

all_quizapi_tags = ['.Net', 'AI', 'AWS', 'Angular', 'BASH',
                    'Blockchain', 'C', 'Css', 'DevOps', 'Docker',
                    'Git', 'HTML', 'Java', 'JavaScript', 'Kubernetes',
                    'Laravel', 'Linux', 'MySQL', 'Node.js', 'PHP',
                    'Python', 'React', 'Ruby', 'Swift', 'Undefined',
                    'VsCode', 'VueJS', 'WordPress', 'dev', 'postgres']


def get_json_quizapi(group, dif, lim):
    request = (f'https://quizapi.io/api/v1/questions?apiKey={PROGRAM_API_TOKEN}'
               f'&category={group}&difficulty={dif}&limit={lim}')
    response = requests.get(request, headers={"User-Agent": ""})
    return response.json()


def get_qa_quizapi(json: list):
    for quest in json:
        try:
            if quest['correct_answer']:
                answ = []
                for let, ans in quest['answers'].items():
                    if ans:
                        answ.append([translator.translate(text=ans)])
            ru_quest = translator.translate(text=quest['question'])
            return ru_quest, answ
        except Exception as e:
            print(e)
            print(json)
            print('-------')
            print(quest)
