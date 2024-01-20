from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.http import require_POST

from network import utils
from network.models import Post


# Create your views here.
def index(request):
    return render(request, 'network/index.html')


@require_POST
@login_required
def create_post(request):
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

    return redirect(reverse('network:index'))
