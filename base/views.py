import os
import random
from datetime import date, datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import redirect, render

from api.views import github_api

from .basic import log, push
from .models import Device, User

INTRO = '''Hello, my name is Jerit. I enjoy building things and have a keen interest in Artificial Intelligence and Machine Learning. If you believe that I could be of assistance to you or would like to connect with me, please don't hesitate to '''


def register_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        name = request.POST['name'].lstrip().rstrip()
        email = request.POST['mail']
        password = request.POST['password1']
        confirm = request.POST['password2']
        name_split = name.split(' ')
        if len(name_split) <= 1:
            messages.error(request, 'Please enter your full name.')
            return render(request, 'base/register.html', {'title': 'Register | Jerit Baiju'})
        first_name = name.split()[0].capitalize()
        last_name = name.split()[1].capitalize()
        if password == confirm:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists.')
                return render(request, 'base/register.html', {'title': 'Register | Jerit Baiju'})
            user = User.objects.create_user(
                email=email, password=password, first_name=first_name, last_name=last_name)
            user.save()
            login(request, user)
            log(request, f"Registered - {name}")
            push(f'Registered - {name}')
            try:
                url = request.POST.get('next')
                cache.clear()
                return redirect(url)
            except:
                cache.clear()
                return redirect('home')
        else:
            messages.error(request, 'Passwords does not match.')
            return render(request, 'base/register.html', {'title': 'Register | Jerit Baiju'})
    else:
        return render(request, 'base/register.html', {'title': 'Register | Jerit Baiju'})


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')
            return render(request, 'base/login.html', {'title': 'Login | Jerit Baiju'})
        user = authenticate(request, email=email, password=password)
        if user is not None:
            log(request, f"Login - {user}")
            login(request, user)
            push(f'Login - {user}')
            try:
                url = request.POST.get('next')
                cache.clear()
                return redirect(url)
            except:
                cache.clear()
                return redirect('home')
        else:
            messages.error(request, 'E-mail OR password does not exit')
            return render(request, 'base/login.html', {'title': 'Login | Jerit Baiju'})
    return render(request, 'base/login.html', {'title': 'Login | Jerit Baiju'})


def logout_page(request):
    push(f"Logout - {request.user}")
    log(request, 'Logout')
    logout(request)
    cache.clear()
    return redirect('home')


@login_required
def register_device(request):
    if request.user.is_superuser:
        device_token = request.GET.get('device_token')
        user = request.user
        device = Device.objects.get_or_create(
            user=user, device_token=device_token)
        device.save()
        return HttpResponse("REGISTERED DEVICE")


def home(request):
    if request.user.is_authenticated:
        if not request.user.is_superuser:
            push(f'Visited - {request.user}')
    else:
        push("Visited - Unknown User")
    log(request, 'Home')
    quotes = [
        {'quote': 'Just turn your Passion into your Profession.',
            'author': 'Jerit Baiju'},
        {'quote': 'The computer was born to solve problems that did not exist before.',
            'author': 'Bill Gates'},
        {'quote': "People don't care about what you say, they care about what you build.",
            'author': 'Mark Zuckerberg'},
        {'quote': "First, solve the problem. Then, write the code.",
            'author': 'John Johnson'},
        {'quote': 'A computer is like a mischievous genie. It will give you exactly what you ask for, but not always what you want.', 'author': 'Joe Sondow'},
        {'quote': 'A good programmer looks both ways before crossing a one-way street.',
         'author': ''},
        {'quote': 'A person who never made a mistake never tried anything new.',
         'author': 'Albert Einstein'},
        {'quote': 'First be Rich, then be a Philosopher', 'author': ''},
        {'quote': 'You will not get a second chance to make the first impression.', 'author': ''},
        {'quote': 'When you look good, you will feel good. When you feel good, you will do good.', 'author': ''},

    ]
    context = {
        'title': 'Jerit Baiju',
        'bio': ['Self-Taught.',
                'Improving Work Ethic.',
                'Passion is my genesis.',
                'Developing new skills everyday.',
                'Yet programming.'],
        'quote': random.choice(quotes),
        'intro': INTRO,
        'skills': [
            'Git', 'Python', 'Heroku', 'Django', 'Project Management', 'Google Search Console',
        ],
        'education': [
            {
                'name': 'Vijayamatha Public School',
                'link': True,
                'url': '/vijayamatha'
            },
            {
                'name': 'MAM Bethany Public School',
                'link': False,
            },
            {
                'name': 'CPM GHSS Peermade',
                'link': False,
            },
            {
                'name': 'GHSS Amaravathy, Kumily',
                'link': False,
            }
        ],
        'firebase': os.environ.get('firebase'),
    }
    return render(request, 'base/index.html', context)


def gallery(request):
    log(request, 'Gallery')
    return redirect('https://jerit-baiju.github.io/gallery/')


def about(request):
    log(request, 'About')
    history = [
        "In 2016, when I was in 4th grade and 10 years old, my parents bought me a laptop. I was ecstatic about it! I quickly learned how to control the cursor and type with ease using MS-Paint and Notepad.",
        "In 2017, I began playing Microsoft's mini-games like Chess, Minesweeper, and others, and learned MS-Logo. I created numerous objects and enjoyed experimenting with them.",
        "In 2018, at the age of 12, I joined an activity on Photoshop and Animation using Adobe Flash-Macromedia. As I explored the computer in my school, I stumbled upon an HTML file and became intrigued. Curious about its purpose, I approached my teacher, Reshmi Miss, and asked about it. She kindly taught me some basics of HTML, sparking my interest in programming.",
        "In 2019, I built my own website using HTML exclusively and subsequently discovered other programming languages such as C++, Python, and JavaScript.",
        "In 2020, I created my own chatbot using Visual Basic and independently upgraded my computer from Windows 7 to Windows 10. I began learning Python and developed simple command-line applications, as well as GUI applications for Windows using Tkinter.",
        "In 2021, I transitioned to Linux and expanded my skills by learning Flask, CSS, and JavaScript. I published my website on PythonAnywhere, which unfortunately is currently unavailable. Additionally, I delved deeper into GIT, REACT, and some Data Science topics. I completed numerous projects including a ChatBot named Clara (web-based) and a Weather app (command-line interface), among others.",
        "In 2022, I acquired proficiency in Django and deployed my website on HEROKU. Additionally, I developed a package called PYFLIT for FLASK users and created projects such as a Weather App (web-based) and a Number Game, among others.",
        "As of 2023, I have begun studying Machine Learning (ML) and Artificial Intelligence (AI), with a particular focus on TensorFlow and Keras, which are currently my primary areas of interest."
    ]
    context = {
        'title': 'About Me',
        'history': history,
        'intro': INTRO
    }
    return render(request, 'base/about.html', context)


def stats(request):
    log(request, 'Stats')
    user = request.user
    github_data = github_api(request)
    today = date.today()
    birthday = datetime.strptime("February 10, 2006", r"%B %d, %Y")
    age = today.year - birthday.year - \
        ((today.month, today.day) < (birthday.month, birthday.day))
    birthday = birthday.strftime(r"%B %d, %Y")
    about_me = [
        {'key': 'age', 'value': age, 'class': 'grey'},
        {'key': 'location', 'value': 'kerala, India', 'class': 'white'},
        {'key': 'D.O.B', 'value': birthday, 'class': 'grey'},
        {'key': 'currently learning',
            'value': 'web development - python', 'class': 'white'},
    ]
    about_web = [
        {'key': 'languages', 'value': 'python, JS, HTML, CSS', 'class': 'grey'},
        {'key': 'Backend', 'value': 'Django | Python', 'class': 'white'},
        {'key': 'packages',
            'value': 'Jinja, BS4, Random, PushBullet', 'class': 'grey'},
        {'key': 'DataBase', 'value': 'SQLITE3', 'class': 'white'},
        {'key': 'Hosted on', 'value': 'AWS', 'class': 'grey'},
        {'key': 'last updated at',
            'value': github_data['updated_at'], 'class': 'white'},
        {'key': 'Stars this repository has on github',
            'value': github_data['stars_this'], 'class': 'grey'}
    ]
    if user.is_authenticated:
        if user.score is None:
            score = 0
        else:
            score = user.score
        about_user = [
            {'key': 'name', 'value': user, 'class': 'grey'},
            {'key': 'e-mail', 'value': user.email, 'class': 'white'},
            {'key': 'score', 'value': score, 'class': 'grey'},
            {'key': 'last login', 'value': user.last_login.date, 'class': 'white'},
            {'key': 'date joined', 'value': user.date_joined.date, 'class': 'grey'},
        ]
    else:
        about_user = 'None'
    stats_data = [
        {'name': 'about me', 'contents': about_me},
        {'name': 'this website', 'contents': about_web},
        {'name': 'about you', 'contents': about_user}
    ]
    github_data = [
        {'key': 'repositories',
            'value': github_data['repositories'], 'class': 'grey'},
        {'key': 'followers',
            'value': github_data['followers'], 'class': 'white'},
        {'key': 'following',
            'value': github_data['following'], 'class': 'grey'},
        {'key': 'total stars earned',
            'value': github_data['stars'], 'class': 'white'},
    ]
    context = {
        'title': 'Stats | Jerit Baiju',
        'stats': stats_data,
        'GitHub': github_data,
        'page': 'stats'
    }
    return render(request, 'base/stats.html', context)


def github(request):
    log(request, 'GitHub')
    return redirect('https://github.com/Jerit-Baiju')


def instagram(request):
    log(request, 'Instagram')
    return redirect('https://www.instagram.com/jerit_baiju')


def whatsapp(request):
    log(request, 'WhatsApp')
    return redirect(r'http://wa.me/+918592060520?text=*Hi Jerit*')


def vijayamatha(request):
    log(request, 'Vijayamatha')
    return redirect('https://vijayamathaschool.in')


def custom_404(request, *args, **kwargs):
    return render(request, '404.html', context={'hr': False}, status=404)


def sitemap(request):
    log(request, 'Sitemap')
    return HttpResponse(open('sitemap.xml').read(), content_type='text/xml')


def robots(request):
    log(request, 'Robots')
    return HttpResponse(open('robots.txt').read(), content_type='text/plain')


def manifest(request):
    return HttpResponse(open('manifest.json').read(), content_type='text/json')


def serviceworker(request):
    return HttpResponse(open('service-worker.js').read(), content_type='text/javascript')


def offline_page(request):
    return render(request, 'offline.html', context={'hr': False})
