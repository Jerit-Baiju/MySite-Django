import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from base.basic import log
from projects.utils import fetch_forks, fetch_stars

# Create your views here.


def projects(request):
    log(request, "Projects")
    projects_data = [
        {
            "name": "a11y-widget",
            "info": "An open-source accessibility tool designed to enhance website inclusivity. Offers "
            "features like text resizing, contrast adjustments, and screen reader support, "
            "helping developers meet WCAG standards with minimal setup.",
            "src": "https://github.com/Jerit-Baiju/a11y-widget",
            "stars": fetch_stars("jerit-baiju/a11y-widget"),
            "forks": fetch_forks("jerit-baiju/a11y-widget"),
        },
        {
            "name": "PyFlit",
            "info": "A powerful Python web development tool that streamlines component creation, "
            "HTML rendering, and asset management. Simplifies Python-to-JavaScript "
            "variable communication for enhanced development workflow.",
            "src": "https://pypi.org/project/pyflit/",
        },
        {
            "name": "MySite",
            "info": "A feature-rich Django-based website showcasing modern web development practices. "
            "Includes comprehensive user management, score tracking, logging systems, and "
            "an intuitive admin interface.",
            "src": "https://github.com/jerit-baiju/mysite-django",
            "stars": fetch_stars("jerit-baiju/mysite-django"),
            "forks": fetch_forks("jerit-baiju/mysite-django"),
        },
        {
            "name": "Number Game",
            "info": "An engaging web-based number guessing game where players have ten attempts to "
            "guess a randomly selected number between 0 and 100. Features score tracking "
            "and user progress monitoring.",
            "src": "/projects/num_game",
        },
        {
            "name": "MAM Bethany Public School",
            "info": "A comprehensive school management system for administrators. Manages "
            "co-curricular activities, teacher operations, documents, school parliament, "
            "and student results with customizable features.",
            "src": reverse("bethany"),
        },
        {
            "name": "Caelium",
            "info": "A versatile platform for personal and group organization. Integrates shared "
            "calendars, interactive maps, video chat, collaborative to-do lists, and blogs "
            "with balanced privacy controls.",
            "src": "https://caelium.co",
        },
    ]
    random.shuffle(projects_data)
    context = {
        "title": "Projects | Jerit Baiju",
        "projects": projects_data,
        "page": "projects",
    }
    return render(request, "projects/projects.html", context)


@login_required(login_url="login-page")
def clara(request):
    log(request, "Clara")
    context = {
        "title": "Clara | Jerit Baiju",
        "name": request.user.first_name,
    }
    return render(request, "projects/clara.html", context)


@login_required(login_url="login-page")
def num_game(request):
    if request.user.score is None:
        score = 0
    else:
        score = request.user.score

    if request.method == "POST":
        context = {"score": score, "win": True, "dark": True, "title": "Number Game"}
        return render(request, "projects/num_game.html", context)
    log(request, "Num Game")
    context = {
        "score": score,
        "title": "Number Game",
        "randint": random.randint(0, 100),
        "dark": True,
    }
    return render(request, "projects/num_game.html", context)


@login_required(login_url="login-page")
def num_game_add(request):
    if request.user.is_authenticated:
        if request.user.score is None:
            score = 0
        else:
            score = request.user.score
        request.user.score = score + 5
        request.user.save()
        log(request, "scored")
        return redirect("num-game")
    messages.error(request, "An unknown error occurred.")
    return redirect("num-game")
