from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import ListView

from network import utils
from network.models import Post


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
        post = Post.objects.get(pk=post_id)
        if user.is_authenticated and post.creator == user:
            post.delete()
            return HttpResponse('Post deleted', status=200)

    return HttpResponse('Unauthorized action', status=401)



class AllPostsView(ListView):
    template_name = 'network/index.html'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'all_posts'
        return context

    def get_queryset(self):
        posts = Post.objects.select_related('creator').all()
        return posts


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
        following_users_posts = Post.objects.select_related('creator').filter(creator__id__in=following_users_ids)

        return following_users_posts
