from django.shortcuts import render
from .extras import get_city, get_score, is_highscore, append_leaderboard, update_average
from .models import HighScore, Average


def index(request):
    return render(request, 'quiz/index.html')


# first render of quiz
def startquiz(request, question_num, scale):
    context = get_city(scale)
    context['question_num'] = question_num
    context['score'] = 0
    context['scale'] = scale
    context['points'] = 11
    return render(request, 'quiz/quiz.html', context=context)


# checks guess and returns points, score and new question
def guess(request, question_num, scale):
    guess = int(request.POST['guess'])
    temp = int(request.POST['temp'])
    score = int(request.POST['score'])
    question_num += 1
    points = get_score(guess, temp)
    score += points

    context = get_city(scale)
    context['question_num'] = question_num
    context['guess'] = guess
    context['prev_temp'] = temp
    context['score'] = score
    context['scale'] = scale
    context['points'] = points

    return render(request, 'quiz/quiz.html', context=context)


# renders results page at the end of quiz
def results(request):
    guess = int(request.POST['guess'])
    temp = int(request.POST['temp'])
    score = int(request.POST['score'])
    update_average(score)
    average = Average.objects.get(pk=1)
    highscore = is_highscore(score)

    context = {
        'score':  score + get_score(guess, temp),
        'average': average.score,
        'highscore': highscore
    }
    return render(request, 'quiz/results.html', context)


# renders leaderboard from results page or navbar
def leaderboard(request):
    if request.method == 'POST':  # user enters via results page
        name = request.POST['name']
        score = request.POST['score']
        print("Hi from views.leaderboard")
        append_leaderboard(score, name)

    # create list of high scorers and get high scores
    highscore_data = HighScore.objects.order_by('-score')

    leaders = []
    for datum in highscore_data:
        leader = {
            'name': datum.name,
            'score': datum.score
        }
        leaders.append(leader)
    context = {
        'leaders': leaders
    }

    return render(request, 'quiz/leaderboard.html', context)

