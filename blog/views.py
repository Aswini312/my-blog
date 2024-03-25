from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from django.utils.html import strip_tags
import math
def post_list(request):
    #posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    posts = Post.objects.all()
    for post in posts:
        # Calculate read time for each post
        post.read_time = calculate_read_time(post.text)
    return render(request, 'blog/post_list.html', {'posts': posts})
    
def calculate_read_time(content):
    # Adjust the average reading speed based on your audience
    average_words_per_minute = 100  # Adjust as needed
    words = len(strip_tags(content).split())  # Count the words in the content
    read_time_minutes = max(1, math.ceil(words / average_words_per_minute))  # Calculate read time
    return read_time_minutes

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    #read_time = post.calculate_read_time()
    return render(request, 'blog/post_detail.html', {'post': post})
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
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})