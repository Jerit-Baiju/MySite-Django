import os
import random
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView

from api.views import github_api, monkey_type_api
from base.content import BIO, HISTORY, INTRO, QUOTES, SKILLS, YEARS

from .basic import log, push
from .models import URL, Document, User, AdminSecret


def register_page(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        name = request.POST["name"].lstrip().rstrip()
        email = request.POST["mail"]
        password = request.POST["password1"]
        confirm = request.POST["password2"]
        name_split = name.split(" ")
        if len(name_split) <= 1:
            messages.error(request, "Please enter your full name.")
            return render(request, "base/register.html", {"title": "Register | Jerit Baiju"})
        first_name = name.split()[0].capitalize()
        last_name = name.split()[1].capitalize()
        if password == confirm:
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.")
                return render(request, "base/register.html", {"title": "Register | Jerit Baiju"})
            user = User.objects.create_user(  # type: ignore
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            user.save()
            login(request, user)
            log(request, f"Registered - {name}")
            push(f"Registered - {name}")
            try:
                url = request.POST.get("next")
                cache.clear()
                return redirect(url)
            except:
                cache.clear()
                return redirect("home")
        else:
            messages.error(request, "Passwords does not match.")
            return render(request, "base/register.html", {"title": "Register | Jerit Baiju"})
    else:
        return render(request, "base/register.html", {"title": "Register | Jerit Baiju"})


def login_page(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")
        try:
            User.objects.get(email=email)
        except:
            messages.error(request, "It seems you want to Sign UP. User does not exist")
            return render(request, "base/login.html", {"title": "Login | Jerit Baiju"})
        user = authenticate(request, email=email, password=password)
        if user is not None:
            log(request, f"Login - {user}")
            login(request, user)
            push(f"Login - {user}")
            try:
                url = request.POST.get("next")
                cache.clear()
                return redirect(url)
            except:
                cache.clear()
                return redirect("home")
        else:
            messages.error(request, "Invalid Password")
            return render(request, "base/login.html", {"title": "Login | Jerit Baiju"})
    return render(request, "base/login.html", {"title": "Login | Jerit Baiju"})


def logout_page(request):
    push(f"Logout - {request.user}")
    log(request, "Logout")
    logout(request)
    cache.clear()
    return redirect("home")


def home(request):
    if request.user.is_authenticated:
        if not request.user.is_superuser:
            push(f"Visited - {request.user}")
    else:
        push("Visited - Unknown User")
    log(request, "Home")
    context = {
        "title": "Jerit Baiju",
        "bio": BIO,
        "quote": random.choice(QUOTES),
        "intro": INTRO,
        "skills": SKILLS,
        "education": [
            {"name": "Vijayamatha Public School", "url": reverse("vijayamatha")},
            {
                "name": "MAM Bethany Public School",
                "url": reverse("bethany"),
            },
            {
                "name": "GHSS Amaravathy Kumily",
            },
            {
                "name": "Marian College Kuttikkanam (BCA)",
                "url": reverse("marian"),
            },
        ][::-1],
        "firebase": os.environ.get("firebase"),
        "resume": Document.objects.get(name="resume"),
    }
    return render(request, "base/index.html", context)


def gallery(request):
    log(request, "Gallery")
    return redirect("https://jerit-baiju.github.io/gallery/")


def about(request):
    log(request, "About")
    context = {"title": "About Me | Jerit Baiju", "history": HISTORY, "intro": INTRO}
    return render(request, "base/about.html", context)


def about_year(request, year):
    log(request, f"About - {year}")
    data = None
    for year_data in YEARS:
        if year_data["year"] == year:
            data = year_data["content"]
    context = {"title": f"About {year} | Jerit Baiju", "year": data}
    return render(request, "base/year.html", context)


def stats(request):
    log(request, "Stats")
    user = request.user
    github_data = github_api(request)
    birthday = datetime.strptime("February 10, 2006", r"%B %d, %Y")
    fmt_birthday = birthday.strftime(r"%B %d, %Y")
    about_me = [
        {"key": "age", "value": ""},
        {"key": "Living in", "value": "kerala, India"},
        {"key": "D.O.B", "value": fmt_birthday},
        {"key": "highest typing Speed", "value": monkey_type_api(), "link": "https://monkeytype.com/profile/Jerit-Baiju"},
        {"key": "currently learning", "value": "AI-ML | TensorFlow"},
    ]
    about_web = [
        {"key": "Backend", "value": "Python | Django"},
        {"key": "Hosted on", "value": "Amazon Web Services"},
        {"key": "last updated at", "value": github_data["updated_at"]},
        {"key": "GitHub Stars Count", "value": github_data["stars_this"]},
    ]
    if user.is_authenticated:
        if user.score is None:
            score = 0
        else:
            score = user.score
        about_user = [
            {"key": "name", "value": user},
            {"key": "e-mail", "value": user.email},
            {"key": "score", "value": score},
            {"key": "last login", "value": user.last_login.date},
            {"key": "date joined", "value": user.date_joined.date},
        ]
    else:
        about_user = "None"
    stats_data = [
        {"name": "about me", "contents": about_me},
        {"name": "this website", "contents": about_web},
        {"name": "about you", "contents": about_user},
    ]
    github_data = [
        {"key": "followers", "value": github_data["followers"]},
        {"key": "following", "value": github_data["following"]},
        {"key": "public repositories", "value": github_data["repositories"]},
        {"key": "total stars earned", "value": github_data["stars"]},
    ]
    context = {
        "title": "Stats | Jerit Baiju",
        "stats": stats_data,
        "GitHub": github_data,
        "page": "stats",
    }
    return render(request, "base/stats.html", context)


def redirector(request, short_code):
    log(request, f"redirect - {short_code}")
    url = URL.objects.get(short_code=short_code)
    url.clicks += 1
    url.save()
    return redirect(url.original_url)


def github(request):
    log(request, "GitHub")
    return redirect("https://github.com/Jerit-Baiju")


def linkedin(request):
    log(request, "LinkedIn")
    return redirect("https://www.linkedin.com/in/jeritbaiju")


def whatsapp(request):
    log(request, "WhatsApp")
    return redirect(r"http://wa.me/+918592060520?text=*Hi Jerit*")


def vijayamatha(request):
    log(request, "Vijayamatha")
    return redirect("https://vijayamathaschool.in")


def marian(request):
    log(request, "Marian College")
    return redirect("https://mariancollege.org/")


def bethany(request):
    log(request, "MAM Bethany")
    return redirect("https://mambethany.com")


def custom_404(request, *args, **kwargs):
    return render(request, "404.html", context={"hr": False}, status=404)


def sitemap(request):
    log(request, "Sitemap")
    return HttpResponse(open("sitemap.xml").read(), content_type="text/xml")


def robots(request):
    log(request, "Robots")
    return HttpResponse(open("robots.txt").read(), content_type="text/plain")


def manifest(request):
    return HttpResponse(open("manifest.json").read(), content_type="application/json")


class ServiceWorkerView(TemplateView):
    content_type = "application/javascript"
    template_name = "js/service-worker.js"


class FirebaseSW(TemplateView):
    content_type = "application/javascript"
    template_name = "js/firebase-sw.js"


def offline_page(request):
    return render(request, "offline.html", context={"hr": False})


def secrets(request):
    password = request.GET.get("pass")
    if password != AdminSecret.objects.get(name="password").secret:
        return JsonResponse({"error": "Invalid password"}, status=403)

    data = AdminSecret.objects.all()
    secrets_dict = {secret.name: secret.secret for secret in data}
    return JsonResponse(secrets_dict)
