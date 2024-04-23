import requests
import random

from support import translator

all_triviaapi_categories = ["music", "sport_and_leisure", "film_and_tv",
                            "arts_and_literature", "history", "society_and_culture",
                            "science", "geography", "food_and_drink", "general_knowledge"]


def get_json_triviaapi():
    request = f'https://the-trivia-api.com/v2/questions'
    response = requests.get(request, headers={"User-Agent": ""})
    return response.json()


def get_qa_triviaapi(json: list, dif):
    for quest in json:
        if quest['difficulty'] == dif:
            answ = quest['incorrectAnswers']
            answ.append(quest['correctAnswer'])
            random.shuffle(answ)
            ru_answ = [[translator.translate(text=a)] for a in answ]
            ru_quest = translator.translate(text=quest['question']['text'])
            return ru_quest, ru_answ
