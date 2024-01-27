from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import DetailView

from .forms import RegistrationForm, ProfileForm


# Create your views here.
def register(request):
    if request.method == 'POST':
        auth_form = RegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if auth_form.is_valid() and profile_form.is_valid():
            user = auth_form.save(commit=False)
            user.set_password(auth_form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'You have successfully signed up!')
            return redirect(reverse('login'))

    else:
        auth_form = RegistrationForm()
        profile_form = ProfileForm()

    return render(request, 'registration/register.html', {'auth_form': auth_form, 'profile_form': profile_form})


@login_required
def user_follow_unfollow(request, username):
    user_model = get_user_model()
    action_user = request.user
    target_user = get_object_or_404(user_model, username=username)

    if request.method == 'POST':
        # User is not allowed to follow themselves
        if action_user != target_user:
            action_user.follows.add(target_user)
            return HttpResponse(status=200)

        else:
            return HttpResponse(status=401)

    if request.method == 'DELETE':
        action_user.follows.remove(target_user)
        return HttpResponse(status=200)

    return HttpResponse(status=405)




@method_decorator(ensure_csrf_cookie, name='dispatch')
class ProfileView(DetailView):
    model = get_user_model()
    context_object_name = 'requested_user'
    template_name = 'network/index.html'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return get_object_or_404(self.model, username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = self.object.posts.annotate(likes_count=Count('likes'))
        posts_paginator = Paginator(posts, 10)
        context['page_obj'] = posts_paginator.get_page(self.kwargs.get('page'))
        context['posts_count'] = posts.count()
        context['following_count'] = self.object.follows.count()
        context['follower_count'] = self.object.followed_by.count()
        context['page'] = 'profile'
        return context
