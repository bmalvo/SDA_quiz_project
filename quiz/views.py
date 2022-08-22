from django.shortcuts import render, redirect
from .api import ApiClient
from .game import Quiz


def index(request):
    try:
        quiz = ApiClient.get_quiz_options()
        return render(request, 'index.html', quiz)
    except ValueError:
        return render(request, 'error.html')


def start_game(request):
    number_of_questions = request.POST['quantity']
    difficulty = request.POST['difficulty']
    category = request.POST['category']
    quiz = Quiz.create_game(number_of_questions, difficulty, category)
    quiz.save(request)
    return redirect('/on_game')


def on_game(request):
    quiz = Quiz.restore(request)
    if not quiz:
        return render(request, 'error.html')

    answer = request.POST.get('answer')
    if answer:
        quiz.check_answer(answer)

    try:
        question = quiz.get_question()
        quiz.save(request)
        return render(request, 'game.html', vars(question))
    except IndexError as x:
        return redirect('/finish')


def finish(request):
    quiz = Quiz.restore(request)
    result = quiz.get_result()
    quiz.stop(request)
    return render(request, 'finish.html', result)
