import os
import random
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView

from api.views import github_api, monkey_type_api

from .basic import log, push
from .models import URL, Document, User

INTRO = ("Hello, my name is Jerit. I enjoy building things and have a keen interest in Artificial Intelligence and "
         "Machine Learning. If you believe that I could be of assistance to you or would like to connect with me, "
         "please don't hesitate to")


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
            user = User.objects.create_user(  # type: ignore
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
            User.objects.get(email=email)
        except:
            messages.error(request, 'It seems you want to Sign UP. User does not exist')
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
            messages.error(request, 'Invalid Password')
            return render(request, 'base/login.html', {'title': 'Login | Jerit Baiju'})
    return render(request, 'base/login.html', {'title': 'Login | Jerit Baiju'})


def logout_page(request):
    push(f"Logout - {request.user}")
    log(request, 'Logout')
    logout(request)
    cache.clear()
    return redirect('home')


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
        {
            'quote': 'A computer is like a mischievous genie. It will give you exactly what you ask for, '
                     'but not always what you want.',
            'author': 'Joe Sondow'},
        {'quote': 'A good programmer looks both ways before crossing a one-way street.', 'author': ''},
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
            'HTML/CSS/JS', 'Bootstrap/Tailwind', 'jQuery', 'Git', 'Python', 'Flask', 'Selenium', 'Django', 'Heroku',
            'SEO', 'GSC', 'AWS', 'DRF', 'React JS', 'Next JS', 'TypeScript',
        ],
        'education': [
            {
                'name': 'Vijayamatha Public School',
                'url': reverse('vijayamatha')
            },
            {
                'name': 'MAM Bethany Public School',
                'url': reverse('bethany'),
            },
            {
                'name': 'CPM GHSS Peermade',
            },
            {
                'name': 'GHSS Amaravathy Kumily',
            }
        ][::-1],
        'firebase': os.environ.get('firebase'),
        'resume': Document.objects.get(name='resume')
    }
    return render(request, 'base/index.html', context)


def gallery(request):
    log(request, 'Gallery')
    return redirect('https://jerit-baiju.github.io/gallery/')


def about(request):
    log(request, 'About')
    history = [
        "In 2016, when I was in 4th grade and 10 years old, my parents bought me a laptop. I was ecstatic about it! I quickly learned how to control the cursor and type with ease using MS-Paint and Notepad.",
        "At 11, I began playing Microsoft's mini-games like Chess, Minesweeper, and others, and learned MS-Logo. I created numerous objects and enjoyed experimenting with them.",
        "At 12, I joined an activity on Photoshop and Animation using Adobe Flash-Macromedia. As I explored the computer in my school, I stumbled upon an HTML file and became intrigued. Curious about its purpose, I approached my teacher, Reshmi Miss, and asked about it. She kindly taught me some basics of HTML, sparking my interest in programming.",
        "At 13, I built my own website using HTML exclusively and subsequently discovered other programming languages such as C++, Python, and JavaScript.",
        "At 14, I created my own chatbot using Visual Basic and independently upgraded my computer from Windows 7 to Windows 10. I began learning Python and developed simple command-line applications, as well as GUI applications for Windows using Tkinter.",
        "At 15, I transitioned to Linux and expanded my skills by learning CSS, JavaScript, GIT, and Flask. I published my website on PythonAnywhere, which unfortunately is currently unavailable. I completed numerous projects including a ChatBot named Clara and a Weather app, among others.",
        "At 16, I acquired proficiency in Django and deployed my website on HEROKU. Additionally, I developed a package called PYFLIT for FLASK users and learned some other languages like Go, R, CPP and Java. ",
        "At 17, I upgraded my setup with a MacBook Air M1, funded by my first freelancing project. This marked my entry into the Apple ecosystem, replacing an old Ubuntu laptop. I optimized my website by deploying it on AWS, and expanded my skills with React.js, Next.js, Tailwind, and TypeScript, adding versatility to my web development expertise.",
        "At 18 (present), I'm navigating towards new horizons in my journey. Aiming to secure a job, I'm strategically honing my skills and exploring opportunities. Embracing growth, I continue to leverage my expertise while maintaining a forward-looking approach. The focus this year revolves around professional development, aligning with my goal of advancing in the ever-evolving tech landscape."
    ]
    context = {
        'title': 'About Me | Jerit Baiju',
        'history': history,
        'intro': INTRO
    }
    return render(request, 'base/about.html', context)


def stats(request):
    log(request, 'Stats')
    user = request.user
    github_data = github_api(request)
    birthday = datetime.strptime("February 10, 2006", r"%B %d, %Y")
    fmt_birthday = birthday.strftime(r"%B %d, %Y")
    about_me = [
        {'key': 'age', 'value': ''},
        {'key': 'location', 'value': 'kerala, India'},
        {'key': 'D.O.B', 'value': fmt_birthday},
        {'key':'highest typing Speed', 'value': monkey_type_api()},
        {'key': 'currently learning',
         'value': 'AI-ML | TensorFlow'},
    ]
    about_web = [
        {'key': 'Backend', 'value': 'Python | Django'},
        {'key': 'Hosted on', 'value': 'Amazon Web Services'},
        {'key': 'last updated at',
         'value': github_data['updated_at']},
        {'key': 'GitHub Stars Count',
         'value': github_data['stars_this']}
    ]
    if user.is_authenticated:
        if user.score is None:
            score = 0
        else:
            score = user.score
        about_user = [
            {'key': 'name', 'value': user},
            {'key': 'e-mail', 'value': user.email},
            {'key': 'score', 'value': score},
            {'key': 'last login', 'value': user.last_login.date},
            {'key': 'date joined', 'value': user.date_joined.date},
        ]
    else:
        about_user = 'None'
    stats_data = [
        {'name': 'about me', 'contents': about_me},
        {'name': 'this website', 'contents': about_web},
        {'name': 'about you', 'contents': about_user}
    ]
    github_data = [
        {'key': 'followers',
         'value': github_data['followers']},
        {'key': 'following',
         'value': github_data['following']},
        {'key': 'public repositories',
         'value': github_data['repositories']},
        {'key': 'total stars earned',
         'value': github_data['stars']},
    ]
    context = {
        'title': 'Stats | Jerit Baiju',
        'stats': stats_data,
        'GitHub': github_data,
        'page': 'stats'
    }
    return render(request, 'base/stats.html', context)


def redirector(request, short_code):
    log(request, f'redirect - {short_code}')
    url = URL.objects.get(short_code=short_code)
    url.clicks += 1
    url.save()
    return redirect(url.original_url)


def github(request):
    log(request, 'GitHub')
    return redirect('https://github.com/Jerit-Baiju')


def linkedin(request):
    log(request, 'LinkedIn')
    return redirect('https://www.linkedin.com/in/jeritbaiju')


def whatsapp(request):
    log(request, 'WhatsApp')
    return redirect(r'http://wa.me/+918592060520?text=*Hi Jerit*')


def vijayamatha(request):
    log(request, 'Vijayamatha')
    return redirect('https://vijayamathaschool.in')


def bethany(request):
    log(request, 'MAM Bethany')
    return redirect('https://mambethany.com')


def custom_404(request, *args, **kwargs):
    return render(request, '404.html', context={'hr': False}, status=404)


def sitemap(request):
    log(request, 'Sitemap')
    return HttpResponse(open('sitemap.xml').read(), content_type='text/xml')


def robots(request):
    log(request, 'Robots')
    return HttpResponse(open('robots.txt').read(), content_type='text/plain')


def manifest(request):
    return HttpResponse(open('manifest.json').read(), content_type='application/json')


class ServiceWorkerView(TemplateView):
    content_type = 'application/javascript'
    template_name = 'js/service-worker.js'


class FirebaseSW(TemplateView):
    content_type = 'application/javascript'
    template_name = 'js/firebase-sw.js'


def offline_page(request):
    return render(request, 'offline.html', context={'hr': False})
