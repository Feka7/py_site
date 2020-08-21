from django.shortcuts import render
from django.utils import timezone
from .models import Articolo
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CreateForm, ReportForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.core.cache import cache
import redis
from django_redis import get_redis_connection

conn = get_redis_connection("default")
HOUR=3600

def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
         return x_forwarded_for.split(',')[0]
    else:
         return request.META.get('REMOTE_ADDR')

def post_list(request):
    posts = Articolo.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Articolo, pk=pk)
    return render(request, 'blog/post_details.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            if post.text.find("hack") < 0:
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                #new operation!!!
                conn.lpush('news',str(timezone.now())+": "+pos.author+' ha pubblicato un post')
                return redirect('post_detail', pk=post.pk)
            else:
                messages.error(request, "Invalid word ---> hack.")

    form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def user_new(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            new_user = User.objects.create_user(user.username, user.email, user.password)
            user.last_name=str(get_ip(request))
            return redirect('../', {})
    else:
        form = CreateForm()
    return render(request, 'blog/new_user.html', {'form': form})

def log(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                #new operation!!!
                conn.lpush('news',str(timezone.now())+f": {username} è online!")
                messages.info(request, f"You are now logged in as {username}")
                ip_now = get_ip(request)
                if str(ip_now) != str(user.last_name):
                    messages.info(request, f"You are now logged with different ip")
                    user.last_name = ip_now
                    user.save()
                return redirect('../')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, "blog/login.html", {"form":form})

def logout_request(request):
    #new operation!!!
    conn.lpush('news',str(timezone.now())+": "+request.user.username+" si è disconnesso!")
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("../")

def post_last_hour(request):
    response = []
    posts = Articolo.objects.filter(published_date__lte=timezone.now(), published_date__gte=timezone.now()-timezone.timedelta(hours=23)).order_by('published_date')
    for post in posts:
        response.append(
            {
                'published_date': post.published_date,
                'title': post.title,
                'author': str(post.author),
            }
        )
    return JsonResponse(response, safe=False)

def report(request):
    if request.method == "GET":
        form = ReportForm(request.GET)
        if form.is_valid():
            s = form.save(commit=False)
            occ = 0
            posts = Articolo.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
            for post in posts:
                occ += post.text.count(str(s.key))
            form = ReportForm()
            return render(request,'blog/report.html', {'form': form, 'occ': occ})
    else:
        form = ReportForm()
    return render(request, 'blog/report.html', {'form': form, 'occ': -1})

def admin_view(request):
    users = User.objects.order_by('username')
    posts = Articolo.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    elems = []
    for user in users:
        occ = 0
        for post in posts:
            if str(user.username) == str(post.author):
                occ += 1
        elems.append(user.username + " ha pubblicato " + str(occ) + " posts")
    return render(request, 'blog/admin_view.html', {'elems': elems })

def utente(request, pk):
    user = get_object_or_404(User, pk=pk)
    posts = Articolo.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    your_posts = []
    for post in posts:
        if str(post.author) == str(user.username):
            your_posts.append(post)

    return render(request, 'blog/utente.html', {'posts': your_posts })
