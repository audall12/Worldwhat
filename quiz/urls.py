from django.urls import path
from quiz import views


app_name = 'quiz'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_num>/<str:scale>/', views.startquiz, name='startquiz'),
    path('<int:question_num>/<str:scale>/guess/', views.guess, name='guess'),
    path('results/', views.results, name='results'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]