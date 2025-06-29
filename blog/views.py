from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, View, CreateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import CommentForm
from .models import Post, Comment

all_posts = Post.objects.all()


class StartingPageView(ListView):
    template_name = 'blog/index.html'
    model = Post
    ordering = ['priority']
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        fetching_data = queryset[:3]
        return fetching_data


class AllPostsView(ListView):
    template_name = 'blog/all_posts.html'
    model = Post
    ordering = ['-date']
    context_object_name = 'all_posts'


class PostDetailView(View):
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get('stored_posts')
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False
        return is_saved_for_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        comments = Comment.objects.filter(post_id=post.id).order_by('-id')
        context = {
            'post': post,
            'tags': post.tags.all(),
            'comment_form': CommentForm(),
            'comments': comments,
            'is_saved': self.is_stored_post(request, post.id),
        }

        return render(request, 'blog/post-detail.html', context)

    def post(self, request, slug):
        post = Post.objects.get(slug=slug)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('post-detail-page', args=[slug]))

        context = {
            'post': post,
            'tags': post.tags.all(),
            'comment_form': CommentForm(),
            'comments': Comment.objects.all().order_by('-id'),
            'is_saved': self.is_stored_post(request, post.id),
        }
        return render(request, 'blog/post-detail.html', context)


class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get('stored_posts')
        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context['posts'] = []
            context['has_posts'] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context['posts'] = posts
            context['has_posts'] = True

        return render(request, 'blog/stored-posts.html', context)

    def post(self, request):
        stored_posts = request.session.get('stored_posts')
        post_id = int(request.POST['post_id'])
        if stored_posts is None:
            stored_posts = []

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)

        request.session['stored_posts'] = stored_posts

        return HttpResponseRedirect('/')

# def index(request):
#     sorted_posts = all_posts.order_by('-date')
#     latest_posts = sorted_posts[:3]
#     return render(request, 'blog/index.html', {
#         'posts': latest_posts
#     })


# def posts(request):
#     return render(request, 'blog/all_posts.html', {
#         'all_posts': all_posts
#     })


# def post_detail(request, slug):
#     identified_post = get_object_or_404(Post, slug=slug)
#     return render(request, 'blog/post-detail.html', {
#         'post': identified_post,
#         'tags': identified_post.tags.all()
#     })
