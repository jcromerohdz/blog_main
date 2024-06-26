
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm
from .models import Post, Category

# Create your views here.
def home(request):
    posts = Post.objects.filter(status=Post.ACTIVE).order_by('-created_at')
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)

def about(request):
    context = {
        'about': 'This is the about page'
    }
    return render(request, 'blog/about.html', context)

def detail(request, category_slug, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.ACTIVE)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

            return redirect('post_detail', slug=slug)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'form': form
    }
    return render(request, 'blog/detail.html', context)

def category(request, slug):
    category = get_object_or_404(Category, slug=slug) 
    posts = category.posts.filter(status=Post.ACTIVE)

    context = {
        'category': category,
        'posts': posts
    }

    return render(request, 'blog/category.html', context)

def search(request):
    query = request.GET.get('query', '')

    posts = Post.objects.filter(status=Post.ACTIVE).filter(Q(title__icontains=query) | Q(intro__icontains=query) | Q(body__icontains=query))

    context = {
        'posts': posts,
        'query': query
    }

    return render(request, 'blog/search.html', context)

