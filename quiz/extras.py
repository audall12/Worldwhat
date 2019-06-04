import json
import random
import requests
import os
import pycountry
from .models import HighScore, Average


def get_key():
    return ''  # insert API key here


# returns a dictionary of random city's data
def get_city(scale):
    # create list of city id numbers
    with open(os.path.dirname(os.path.realpath(__file__)) + '/files/quiz/cityid.json', encoding='utf8') as infile:
        data = json.load(infile)
        infile.close()

    # call API with random city id
    city_id = data[random.randint(0, 209578)]
    parameters = {'id': city_id, 'APPID': get_key()}
    try:
        response = requests.get("https://api.openweathermap.org/data/2.5/weather", params=parameters)
        response.raise_for_status()
    except requests.RequestException:
        return None

    response = response.json()

    # get country's name from 2 letter or 3 letter code
    try:
        country = pycountry.countries.get(alpha_2=response['sys']['country'])
    except KeyError:
        country = pycountry.countries.get(alpha_3=response['sys']['country'])

    # check and convert celsius
    if scale == 'celsius':
        temp = round(response['main']['temp'] - 273.15)
    else:
        temp = round((9/5) * (response['main']['temp'] - 273.15) + 32)

    city = {
        'name': response['name'],
        'country_code': country.name,
        'temp': temp
    }

    return city


# returns score of current question
def get_score(guess, target):
    abs_v = abs(guess - target)
    if abs_v > 5:
        return 0

    # calculate score as distance from target answer
    score = 5 - abs_v

    # return double if guessed correctly
    if score == 5:
        return 10

    return score


# checks if score can enter leaderboard
def is_highscore(score):
    # get lowest score on leader-board
    count = HighScore.objects.count()

    # check leader-board is full
    if count < 10:
        return True

    # else check score against lowest score on leaderboard
    else:
        last = HighScore.objects.order_by('-score')[9]
        if last.score < score:
            return True

    return False


# add user to leaderboard
def append_leaderboard(score, name):
    # check leader-board is full
    count = HighScore.objects.count()
    if count == 10:
        last = HighScore.objects.order_by('-score')[9]
        last.score = score
        last.name = name
        last.save()
    else:
        newScore = HighScore(score=score, name=name)
        newScore.save()


# updates average score
def update_average(score):
    # check average score exists
    try:
        data = Average.objects.get(pk=1)
    except Average.DoesNotExist:
        average = Average(score=score, games=1)
        average.save()
        return

    # else update average
    average = data.score
    games = data.games
    new_average = (games*(average/(games + 1))) + (score/(games + 1))
    data.score = new_average
    data.games += 1
    data.save()

