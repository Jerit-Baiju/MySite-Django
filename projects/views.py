import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from base.basic import log


# Create your views here.


def projects(request):
    log(request, "Projects")
    projects_data = [
        {
            "name": "PyFlit",
            "info": "This dynamic tool has significantly streamlined my development process, allowing "
            "me to effortlessly add components, render HTML, incorporate CSS and JS, "
            "and seamlessly send Python variables to JavaScript.",
            "src": "https://pypi.org/project/pyflit/",
        },
        # {'name': 'Clara', 'info': 'CHAT-BOT made with CHAT-BOT-API. Simple STATIC Project.',
        #     'src': '/projects/clara'},
        {
            "name": "MySite",
            "info": "DYNAMIC WEBSITE made with DJANGO framework, FEATURES - Admin Panel, "
            "User Management, User-Score Handling, LOGS, etc.. ",
            "src": "https://github.com/jerit-baiju/mysite-django",
        },
        {
            "name": "Number Game",
            "info": "You should assume the number that is picked from 0-100 randomly by computer "
            "with TEN chances.",
            "src": "/projects/num_game",
        },
        {
            "name": "MAM Bethany Public School",
            "info": "Developed for administrators, it enables easy management of "
            "co-curricular activities, image customization, "
            "teacher operations, document handling, school parliament "
            "details, management, and result tracking. ",
            "src": reverse("bethany"),
        },
        {
            "name": "Caelium",
            "info": "Caelium is an all-in-one platform for organizing personal, family, couple, and work activities, currently under development. It includes features like a shared calendar, interactive map, chat with video calls, shared to-do lists, blogs, and more, ensuring equal privacy and functionality for all users",
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
