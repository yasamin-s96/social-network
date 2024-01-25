import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core import serializers
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import ListView
from django.urls import reverse
from django.utils.decorators import method_decorator

from network import utils
from network.models import Post, Comment


# Create your views here.

@require_POST
@login_required
def post_create(request):
    text = request.POST.get('text')
    picture = request.FILES.get('picture')

    if not (text or picture):
        messages.error(request, 'Error: the post can not be entirely empty.')

    else:
        try:
            utils.manage_post_creation(request.user, text, picture)
        except ValidationError as e:
            utils.manage_exception_object(request, e)
        else:
            messages.success(request, 'Post created successfully.')

    return redirect(reverse('network:posts_list'))


@login_required
def post_delete(request, post_id):
    if request.method == 'DELETE':
        user = request.user
        post = get_object_or_404(Post, pk=post_id)
        if user.is_authenticated and post.creator == user:
            post.delete()
            return HttpResponse('Post deleted', status=200)

    return HttpResponse('Unauthorized action', status=401)


@login_required
def post_like_unlike(request, post_id):
    user = request.user
    post = get_object_or_404(Post, pk=post_id)

    # Perform like
    if request.method == 'POST':
        if user not in post.likes.all():
            post.likes.add(user)
            return HttpResponse(f'Post liked by {user}', status=200)

    # Perform unlike
    if request.method == 'DELETE':
        if user in post.likes.all():
            post.likes.remove(user)
            return HttpResponse(f'Post unliked by {user}', status=200)

    return HttpResponse(status=400)


@login_required
def post_save_unsave(request, post_id):
    user = request.user
    post = get_object_or_404(Post, pk=post_id)

    # Perform save
    if request.method == 'POST':
        if user not in post.saved_by.all():
            post.saved_by.add(user)
            return HttpResponse(f'Post saved by {user}', status=200)

    # Perform unsave
    if request.method == 'DELETE':
        if user in post.saved_by.all():
            post.saved_by.remove(user)
            return HttpResponse(f'Post unsaved by {user}', status=200)

    return HttpResponse(status=400)


def post_comments(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        comment = json.loads(request.body.decode('utf-8'))
        comment = Comment.objects.create(user=request.user, content=comment['comment_text'], post=post)
        return JsonResponse([comment.serialize()], safe=False)

    comments = post.comments.all()
    data = [comment.serialize() for comment in comments]
    return JsonResponse(data, safe=False)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class AllPostsView(ListView):
    template_name = 'network/index.html'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'all_posts'
        return context

    def get_queryset(self):
        posts = Post.objects.annotate(likes_count=Count('likes')).select_related('creator').prefetch_related('likes')
        return posts


@method_decorator(ensure_csrf_cookie, name='dispatch')
class FollowingPostsView(LoginRequiredMixin, ListView):
    template_name = 'network/index.html'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'following'
        return context

    def get_queryset(self):
        user = self.request.user
        following_users_ids = user.follows.values_list('id', flat=True)
        following_users_posts = Post.objects.annotate(likes_count=Count('likes')).select_related('creator') \
            .prefetch_related('likes').filter(creator__id__in=following_users_ids)

        return following_users_posts


@method_decorator(ensure_csrf_cookie, name='dispatch')
class SavedPostsView(LoginRequiredMixin, ListView):
    template_name = 'network/index.html'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'saved'
        return context

    def get_queryset(self):
        user = self.request.user
        saved_posts = Post.objects.annotate(likes_count=Count('likes')).select_related('creator') \
            .prefetch_related('likes').filter(saved_by=user)

        return saved_posts
