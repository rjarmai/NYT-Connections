from classes import *
import json

YELLOW = '#F9DF6D'
GREEN = '#A0C35A'
BLUE = '#B0C4EF'
PURPLE = '#BA81C5'
LANGUAGE = 'eng'

source_file = f"categories_{LANGUAGE}.json"

with open(source_file, encoding='utf-8') as file:
    data = json.load(file)

word_list = random.choice(data)
cat1 = word_list['category1']
cat2 = word_list['category2']
cat3 = word_list['category3']
cat4 = word_list['category4']

category1 = Category(words=cat1["words"], color=cat1["color"], explanation=cat1["explanation"])
category2 = Category(words=cat2["words"], color=cat2["color"], explanation=cat2["explanation"])
category3 = Category(words=cat3["words"], color=cat3["color"], explanation=cat3["explanation"])
category4 = Category(words=cat4["words"], color=cat4["color"], explanation=cat4["explanation"])
categories = [category1, category2, category3, category4]

game = ConnectionsGame(categories)

