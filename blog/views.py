import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from .forms import PostForm
from .models import Post, Category
from django.db.models import Q


def dummy():
    return str(random.randint(1, 10))


def get_categories():
    all = Category.objects.all()
    count = all.count()
    half = count // 2 + 1
    return {"cat1": all[:half], "cat2": all[half:]}


# Create your views here.
def index(request):
    # posts = Post.objects.all()
    # posts = Post.objects.filter(title__contains='python')
    # posts = Post.objects.filter(published_date__year=2023)
    # posts = Post.objects.filter(category__name__iexact='python')
    posts = Post.objects.order_by('-published_date')
    # post = Post.objects.get(pk=2)
    context = {'posts': posts}
    context.update(get_categories())

    return render(request, "blog/index.html", context=context)


def post(request, id=None):
    post = get_object_or_404(Post, pk=id)
    context = {"post": post}
    context.update(get_categories())

    return render(request, "blog/post.html", context=context)


def category(request, name=None):
    c = get_object_or_404(Category, name=name)
    posts = Post.objects.filter(category=c).order_by('-published_date')
    context = {"posts": posts}
    context.update(get_categories())

    return render(request, "blog/index.html", context=context)


def about(request):
    return render(request, "blog/about.html")


def contacts(request):
    return render(request, "blog/contacts.html")


def services(request):
    return render(request, "blog/services.html")


def pro_url(request, dynamic_url):
    print(dynamic_url)
    return render(request, "blog/services.html", context={"url": dynamic_url})


def search(request):
    query = request.GET.get('query')
    posts = Post.objects.filter(Q(content__icontains=query) | Q(title__icontains=query))
    context = {"posts": posts}
    context.update(get_categories())

    return render(request, "blog/index.html", context=context)


@login_required
def create(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = now()
            post.user = request.user
            post.save()
            return index(request)
    context = {"form": form}
    return render(request, "blog/create.html", context=context)


@login_required
def profile(request):
    context = {"user": request.user}
    return render(request, "blog/profile.html", context=context)


