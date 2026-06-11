from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, BlogForm
from .models import Blog


def home(request):
    blogs = Blog.objects.all()
    return render(request, 'home.html', {'blogs': blogs})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = RegisterForm()

    return render(
        request,
        'registration/register.html',
        {'form': form}
    )


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')

    else:
        form = AuthenticationForm()

    return render(
        request,
        'registration/login.html',
        {'form': form}
    )


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def create_blog(request):

    if request.method == 'POST':
        form = BlogForm(request.POST)

        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()

            return redirect('home')

    else:
        form = BlogForm()

    return render(
        request,
        'create_blog.html',
        {'form': form}
    )


@login_required
def edit_blog(request, blog_id):

    blog = get_object_or_404(
        Blog,
        id=blog_id,
        author=request.user
    )

    if request.method == 'POST':
        form = BlogForm(
            request.POST,
            instance=blog
        )

        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = BlogForm(instance=blog)

    return render(
        request,
        'edit_blog.html',
        {'form': form}
    )


@login_required
def delete_blog(request, blog_id):

    blog = get_object_or_404(
        Blog,
        id=blog_id,
        author=request.user
    )

    blog.delete()

    return redirect('home')