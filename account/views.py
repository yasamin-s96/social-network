from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import RegistrationForm


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'You have successfully signed up!')
            return redirect(reverse('account:login'))

    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})
