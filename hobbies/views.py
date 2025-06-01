from django.shortcuts import render, redirect
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import SignUpForm
from django.contrib.auth import login
from .models import Post, Comment, Like, Category
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import CommentForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  
            post.save()
            return redirect('home')  
    else:
        form = PostForm()
    return render(request, 'hobbies/create_post.html', {'form': form})

from django.shortcuts import render, get_object_or_404

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    return render(request, 'hobbies/home.html', {
        'posts': posts,
        'categories': categories,
    })


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-created_at')

    form = CommentForm()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post.id)

    # Check if the user has liked the post
    user_liked = False
    if request.user.is_authenticated:
        user_liked = post.like_set.filter(user=request.user).exists()

    return render(request, 'hobbies/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'user_liked': user_liked,
    })


@login_required
def profile(request):
    user_posts = Post.objects.filter(user=request.user)
    liked_posts = Post.objects.filter(like__user=request.user)

    return render(request, 'hobbies/profile.html', {
        'user_posts': user_posts,
        'liked_posts': liked_posts,
    })


@login_required
def like_toggle(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)

    if not created:
        # toggle like
        like.delete()
    return HttpResponseRedirect(reverse('post_detail', args=[post_id]))


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(category=category).order_by('-created_at')

    return render(request, 'hobbies/category_detail.html', {
        'category': category,
        'posts': posts
    })