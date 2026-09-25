import json
import os
from datetime import datetime

import pytz
import requests
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv

from api.models import ImageUpload
from base import basic
from base.models import AdminLog, AdminSecret

load_dotenv()
# Create your views here.


@csrf_exempt
def subscribe(request):
    if request.user.is_superuser:
        if request.method == "POST":
            try:
                token = request.POST.get("token")
                token_object = AdminSecret.objects.get(name="token")
                token_object.secret = token
                token_object.save()
                return JsonResponse({"status": "UPDATED SUCCESSFULLY"})
            except:
                try:
                    token = request.POST.get("token")
                    token_object = AdminSecret.objects.create(name="token", secret=token)
                    token_object.save()
                    return JsonResponse({"status": "CREATED SUCCESSFULLY"})
                except:
                    return JsonResponse({"status": "FAILED"})
        return render(request, "api/subscribe.html", {"dark": True, "firebase_key": os.environ["firebase"]})
    return JsonResponse({"status": "Access Denied"})


def latest_log(request):
    email = request.GET.get("email")
    password = request.GET.get("pass")
    if email == "jeritalumkal@gmail.com":
        user = authenticate(request, email=email, password=password)
    else:
        user = None
    if user is not None:
        context = {"title": "Latest Log", "dark": True, "content": AdminLog.objects.get(name="api_log").latest_log}
        return render(request, "api/main.html", context)
    else:
        context = {"title": "Latest Log", "dark": True, "content": "Access Denied"}
        return render(request, "api/main.html", context)


def logs(request, page):
    if request.user.is_superuser:
        page = max(page, 1)
        all_logs = str(AdminLog.objects.get(name="api_log").log).split("\n")
        # Split logs into pages with 20 logs per page
        paginator = Paginator(all_logs, 20)
        # Get the logs for the requested page
        page_obj = paginator.get_page(page)
        context = {
            "title": "Jerit Baiju | Logs",
            "dark": True,
            "content": page_obj,  # Pass the logs for the requested page to the template
            "type": "list",
            "page": page,
            "next": page + 1,
            "previous": max(page - 1, 1),
        }
        return render(request, "api/main.html", context)
    context = {"title": "Latest Log", "dark": True, "content": "Access Denied"}
    return render(request, "api/main.html", context)


def clr_admin_log(request):
    email = request.GET.get("email")
    password = request.GET.get("pass")
    if email == "jeritalumkal@gmail.com":
        user = authenticate(request, email=email, password=password)
    else:
        user = None
    if user is not None:
        api_log = AdminLog.objects.get(name="api_log")
        api_log.log = ""
        api_log.save()
        basic.push("API LOG CLEARED")
        context = {"title": "Latest Log", "dark": True, "content": "Cleared"}
        return render(request, "api/main.html", context)
    context = {"title": "Latest Log", "dark": True, "content": "Access Denied"}
    return render(request, "api/main.html", context)


def github_api(request):
    basic.log(request, "github-api-fetch")
    auth = ("jerit-baiju", os.environ["github_api"])
    try:
        update_url = "https://api.github.com/repos/jerit-baiju/mysite-django"
        github_url = "https://api.github.com/users/jerit-baiju"
        repos_url = "https://api.github.com/users/jerit-baiju/repos"
        updated_at = requests.get(update_url, auth=auth, timeout=10).json()["pushed_at"]
        github = requests.get(github_url, auth=auth, timeout=10).json()
        repos = requests.get(repos_url, auth=auth, timeout=10).json()
        stars = 2
        for repo in repos:
            stars += repo["stargazers_count"]
        update_date = datetime.strptime(updated_at, r"%Y-%m-%dT%H:%S:%fZ")
        update = update_date.astimezone(pytz.timezone("Asia/Kolkata")).strftime(r"%B %d, %Y")
        repositories = github["public_repos"]
        followers = github["followers"]
        following = github["following"]
        data = {
            "updated_at": update,
            "repositories": repositories,
            "followers": followers,
            "following": following,
            "stars": stars,
        }
        cache.set("github_data", data, timeout=24 * 60 * 60)
        return data
    except:
        data = cache.get("github_data")
        if not data:
            data = {
                "updated_at": "update",
                "repositories": "repositories",
                "followers": "followers",
                "following": "following",
                "stars": "stars",
            }
        return data


def monkey_type_api():
    try:
        url = "https://api.monkeytype.com/users/personalBests/"
        querystring = {"mode": "words", "mode2": "10"}
        headers = {
            "Authorization": f"ApeKey {os.environ['monkey_type']}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/46.0.2490.80",
        }
        response = requests.get(url, headers=headers, params=querystring, timeout=10).json()
        wpm = round(float(response["data"][0]["wpm"]))
        if not wpm:
            raise ValueError("Invalid WPM received from Monkey")
        cache.set("wpm", wpm, 60 * 5)
        return f"{wpm} WPM"
    except:
        wpm = cache.get("wpm")
        return wpm if wpm else "WPM"


@csrf_exempt  # Use this decorator if you're not using CSRF tokens for simplicity.
def upload_image(request):
    if request.method == "POST" and request.FILES.get("image"):
        image = request.FILES["image"]
        image_file = ImageUpload.objects.create(image=image)
        image_file.save()
        return JsonResponse({"message": "Image uploaded successfully"}, status=201)
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)


NLP_DATA_FILE = os.path.join(os.path.dirname(__file__), "nlp_data.json")


def load_nlp_data():
    if os.path.exists(NLP_DATA_FILE):
        with open(NLP_DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def nlp_code(request, pid):
    data = load_nlp_data()
    pid_str = str(pid).strip()
    if pid_str.isdigit():
        pid_key = str(int(pid_str))
    else:
        pid_key = pid_str.lower()

    problem = data.get(pid_key)
    if not problem:
        return HttpResponse("Problem not found\n", status=404, content_type="text/plain; charset=utf-8")

    if isinstance(problem, dict):
        code = problem.get("code", "")
    else:
        code = str(problem)

    if not code.endswith("\n"):
        code += "\n"

    return HttpResponse(code, content_type="text/plain; charset=utf-8")


def nlp_list(request):
    data = load_nlp_data()
    problems = []
    for k in sorted(data.keys(), key=lambda x: int(x) if x.isdigit() else 999):
        if k == "setup":
            continue
        item = data[k]
        problems.append({
            "id": item.get("id"),
            "title": item.get("title"),
            "url": f"/api/nlp/{k}",
        })
    return JsonResponse({"problems": problems})


NLP_PY_FILE = os.path.join(os.path.dirname(__file__), "nlp.py")


def nlp_py(request):
    if os.path.exists(NLP_PY_FILE):
        with open(NLP_PY_FILE, "r", encoding="utf-8") as f:
            code = f.read()
        return HttpResponse(code, content_type="text/plain; charset=utf-8")
    return HttpResponse("File not found\n", status=404, content_type="text/plain; charset=utf-8")

