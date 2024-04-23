import requests
import random

from support import translator

all_opentdb_categories = {'General Knowledge': 1,
                          'Entertainment: Books': 10,
                          'Entertainment: Film': 11,
                          'Entertainment: Music': 12,
                          'Entertainment: Musicals & Theatres': 13,
                          'Entertainment: Television': 14,
                          'Entertainment: Video Games': 15,
                          'Entertainment: Board Games': 16,
                          'Science & Nature': 17,
                          'Science: Computers': 18,
                          'Science: Mathematics': 19,
                          'Mythology': 20,
                          'Sports': 21,
                          'Geography': 22,
                          'History': 23,
                          'Politics': 24,
                          'Art': 25,
                          'Celebrities': 26,
                          'Animals': 27,
                          'Vehicles': 28,
                          'Entertainment: Comics': 29,
                          'Science: Gadgets': 30,
                          'Entertainment: Japanese Anime & Manga': 31,
                          'Entertainment: Cartoon & Animations': 32
                          }


def get_json_opentdb(group, dif, kind, lim):
    request = (f'https://opentdb.com/api.php?amount={lim}&'
               f'category={all_opentdb_categories[group]}&difficulty={dif}&type={kind}')
    response = requests.get(request)
    return response.json()


def get_qa_opentdb(json):
    for quest in json['results']:
        answ = quest['incorrect_answers']
        answ.append(quest['correct_answer'])
        random.shuffle(answ)
        ru_answ = [[translator.translate(text=a)] for a in answ]
        ru_quest = translator.translate(text=quest['question'])
        return ru_quest, ru_answ
