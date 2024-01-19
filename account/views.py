from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

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
