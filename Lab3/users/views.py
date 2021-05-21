from django.shortcuts import render, reverse
from django.views.generic.detail import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from .forms import SignInForm, SignUpForm
from django.contrib import messages
from cart.models import Cart
from .models import UserProfile


class SignInView(View):

    def get(self, request, *args, **kwargs):
        form = SignInForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = authenticate(email=cleaned_data['email'], password=cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('products:home'))
                else:
                    messages.error(request, 'Аккунт пользователя неактивен')
            else:
                messages.error(request, 'Такого пользователя не существует')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class SignUpView(View):

    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            cleaned_data = form.cleaned_data
            user = authenticate(email=cleaned_data['email'], password=cleaned_data['password1'])
            login(request, user)
            Cart.objects.create(user=user)
            UserProfile.objects.create(user=user, address=cleaned_data.get('address'),
                                       first_name=cleaned_data.get('first_name'),
                                       last_name=cleaned_data.get('last_name'),
                                       phone_number=cleaned_data.get('phone_number'))
            return HttpResponseRedirect(reverse('products:home'))
        messages.error(request, form.errors)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class SignOutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
