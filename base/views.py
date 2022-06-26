import random
from datetime import datetime

import pytz
import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect, render
from pushbullet import Pushbullet

from .models import AdminLog, AdminSecret, User

try:
    pb_key, _ = AdminSecret.objects.get_or_create(name='pushbullet')
except:
    None


def push(text):
    try:
        text = str(text).capitalize()
        pb = Pushbullet(pb_key.secret)
        pb.push_note("MySite", text, pb.devices[0])
    except:
        None


def log(request, data):
    date = datetime.now(pytz.timezone("Asia/Kolkata")).date()
    time = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%H:%M")
    agent = request.META['HTTP_USER_AGENT']
    admin_log, _ = AdminLog.objects.get_or_create(name='api_log')

    if request.user.is_authenticated:
        user = request.user
        body = f"{date} | {time} | {user} | {data} | {agent}"
        admin_log.latest_log = body
        admin_log.log = f"{body}\n{admin_log.log}"
        admin_log.save()
        user_log = f"{date} | {time} | {data} | {agent}\n{user.log}"
        user.log = user_log
        user.save()
    else:
        body = f"{date} | {time} | {data} | {agent}"
        admin_log.latest_log = body
        admin_log.log = f"{body}\n{admin_log.log}"
        admin_log.save()


intro = '''Hi, I'm Jerit. I am passionate about Coding and building things. I am
particularly interested in projects that touch Artificial Intelligence,
Web Development, Chatbot, Django. If you think I can be helpful to you or would
like to meet me, please feel free to'''


def registerPage(request):
    if request.method == 'POST':
        name = request.POST['name']
        username = str(request.POST['username']).lower().lstrip().rstrip()
        mail = request.POST['mail']
        password = request.POST['password1']
        confirm = request.POST['password2']
        name_split = name.split()
        if len(name_split) < 1:
            messages.error(request, 'Please enter your full name')
            return render(request, 'base/register.html', {'title': 'Register | Jerit Baiju'})
        else:
            first_name = name.split()[0].capitalize()
            last_name = name.split()[1].capitalize()
        if " " in username:
            messages.error(request, 'Username must not contain space')
            return render(request, 'base/register.html', {'title': 'Register | Jerit Baiju'})
        elif password == confirm:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
                return render(request, 'base/register.html', {'title': 'Register | Jerit Baiju'})
            elif User.objects.filter(email=mail).exists():
                messages.error(request, 'Email already exists')
                return render(request, 'base/register.html', {'title': 'Register | Jerit Baiju'})
            else:
                user = User.objects.create_user(
                    username=username, password=password, email=mail, name=name, first_name=first_name, last_name=last_name)
                user.save()
                login(request, user)
                push(f'Registered - {name}')
                try:
                    url = request.POST.get('next')
                    return redirect(url)
                except:
                    return redirect('home')
        else:
            messages.error(request, 'Passwords does not match')
            return render(request, 'base/register.html', {'title': 'Register | Jerit Baiju'})
    else:
        return render(request, 'base/register.html', {'title': 'Register | Jerit Baiju'})


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
            return render(request, 'base/login.html', {'title': 'Login | Jerit Baiju'})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            push(f'Login - {user.name}')
            try:
                url = request.POST.get('next')
                return redirect(url)
            except:
                return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')
            return render(request, 'base/login.html', {'title': 'Login | Jerit Baiju'})
    return render(request, 'base/login.html', {'title': 'Login | Jerit Baiju'})


def logoutPage(request):
    push(f"Logout - {request.user.name}")
    log(request, 'Logout')
    logout(request)
    return redirect('home')


def home(request):
    if request.user.is_authenticated:
        if request.user.username != 'jerit':
            push(f'Visited - {request.user.name}')
    else:
        push(f'Visited - Unknown User')
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
        {'quote': 'A computer is like a mischievous genie. It will give you exactly what you   ask for, but not always what  you want.', 'author': 'Joe Sondow'},
        {'quote': 'A good programmer looks both ways before crossing a onw-way street.',
         'author': 'Unknown'},
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
                'Struggling for financial freedom.'],
        'quote': random.choice(quotes),
        'intro': intro,
        'skills': [
            'Git', 'Python', 'Heroku', 'Django', 'Flask', 'Jupyter', 'Project Management', 'Google Search Console',
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
            }
        ]

    }
    return render(request, 'base/index.html', context)


def gallery(request):
    log(request, 'Gallery')
    return redirect('https://jeritbaiju.herokuapp.com')


def about(request):
    log(request, 'About')
    history = [
        "2016 - I was 10 years old studying in 4th class, my parents bought me a laptop. I was so excited about it. I learned to control the cursor and to type easily with MS-PAINT, NOTEPAD.",
        "2017 - Started to play the MS mini games like CHESS, MINESWEEPER etc. And learned MS-LOGO, created many objects and played with them.",
        "2018 - I was 12. Joined for the activity PHOTOSHOP AND ANIMATION with Adobe Flash-Macromedia. Started to search every files and locations on computer in my school. Unexpectedly opened an HTML file and I thought it was programming, I asked to my teacher (Reshmi miss) about it and she taught me some basics of HTML.",
        "2019 - I created my own website using HTML only. Heard about programming languages(C++, Python, JavaScript).",
        "2020 - Made my own chatbot using VISUAL BASIC. I upgraded my computer windows 7 to windows 10 alone. Started to learn python, made simple command line applications. I made GUI apps for windows using Tkinter.",
        "2021 - Switched to Linux. Learned Flask, CSS, JavaScript. I published my website on PythonAnywhere (currently not available). Learned GIT, REACT and some DS. Made many projects like ChatBot named Clara (WEB), Weather app (CLI)",
        "2022 - Learned Django and hosted my website on HEROKU. Made a Package called PYFLIT for FLASK users, and created projects Weather App (WEB), NUM GAME etc. Currently working on Django + React."
    ]
    context = {
        'title': 'About Me',
        'history': history,
        'intro': intro
    }
    return render(request, 'base/about.html', context)


def stats(request):
    log(request, 'Stats')
    user = request.user
    update_url = 'https://api.github.com/repos/jerit-baiju/mysite-django'
    updated_at = requests.get(update_url).json()['pushed_at']
    date = datetime.strptime(updated_at, r"%Y-%m-%dT%H:%S:%fZ")
    update = date.astimezone(pytz.timezone(
        "Asia/Kolkata")).strftime(r"%d %b %Y")
    about_me = [
        {'key': 'age', 'value': '16', 'class': 'grey'},
        {'key': 'current city', 'value': 'kerala, India', 'class': 'white'},
        {'key': 'birthday', 'value': '10 February 2006', 'class': 'grey'},
        {'key': 'started coding on', 'value': '2018', 'class': 'white'},
        {'key': 'currently learning',
            'value': 'web development - python', 'class': 'grey'},
        {'key': 'OS', 'value': 'Ubuntu', 'class': 'white'},
    ]
    about_web = [
        {'key': 'languages', 'value': 'python, JS, HTML, CSS', 'class': 'grey'},
        {'key': 'Backend', 'value': 'Django | Python', 'class': 'white'},
        {'key': 'packages',
            'value': 'Jinja, BS4, Random, PushBullet', 'class': 'grey'},
        {'key': 'DataBase', 'value': 'SQLITE3', 'class': 'white'},
        {'key': 'Hosted on', 'value': 'Heroku', 'class': 'grey'},
        {'key': 'last updated at', 'value': update, 'class': 'white'}
    ]
    if user.is_authenticated == True:
        about_user = [
            {'key': 'name', 'value': user.name, 'class': 'grey'},
            {'key': 'username', 'value': user.username, 'class': 'white'},
            {'key': 'e-mail', 'value': user.email, 'class': 'grey'},
            {'key': 'score', 'value': user.score, 'class': 'white'},
            {'key': 'last login', 'value': user.last_login.date, 'class': 'grey'},
            {'key': 'date joined', 'value': user.date_joined.date, 'class': 'white'},
        ]
    else:
        about_user = [
            {'key': 'authenticated', 'value': 'not', 'class': 'grey'},
            {'key': 'note', 'value': 'please login to see all the details', 'class': 'white'}
        ]
    stats = [
        {'name': 'some stats about me', 'contents': about_me},
        {'name': 'some stats about this website', 'contents': about_web},
        {'name': 'some stats about you', 'contents': about_user}
    ]
    context = {
        'title': 'Stats | Jerit Baiju',
        'stats': stats,
    }
    return render(request, 'base/stats.html', context)


def sitemap(request):
    log(request, 'Sitemap')
    return HttpResponse(open('sitemap.xml').read(), content_type='text/xml')


def robots(request):
    log(request, 'Robots')
    return HttpResponse(open('robots.txt').read(), content_type='text/plain')


def github(request):
    log(request, 'GitHub')
    return redirect('https://github.com/Jerit-Baiju')


def instagram(request):
    log(request, 'Instagram')
    return redirect('https://www.instagram.com/jerit_baiju')


def whatsapp(request):
    log(request, 'Whatsapp')
    return redirect(r'http://wa.me/+918592060520?text=*Hi Jerit*')
    # %F0%9F%91%8B%F0%9F%8F%BB


def vijayamatha(request):
    log(request, 'Vijayamatha')
    return redirect('https://vijayamathaschool.in')
