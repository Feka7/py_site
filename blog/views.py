from django.shortcuts import render
from django.utils import timezone
from .models import Articolo
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CreateForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def post_list(request):
    posts = Articolo.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Articolo, pk=pk)
    return render(request, 'blog/post_details.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def user_new(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            new_user = User.objects.create_user(user.username, user.email, user.password)
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
                messages.success(request, f"You are now logged in as {username}")
                return redirect('../')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, "blog/login.html", {"form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("../")
