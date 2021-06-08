from django.shortcuts import render, reverse
from django.views.generic.detail import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from .forms import SignInForm, SignUpForm
from django.contrib import messages
from cart.models import Cart
from .models import UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin
import logging
import asyncio
from .async_requests import *

logger = logging.getLogger(__name__)


class SignInView(View):

    def get(self, request, *args, **kwargs):
        form = SignInForm()
        logger.info(f"Loading sign in view")
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = authenticate(email=cleaned_data['email'], password=cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    logger.info(f"User {cleaned_data['email']} signed in")
                    return HttpResponseRedirect(reverse('products:home'))
                else:
                    messages.error(request, 'Аккунт пользователя неактивен')
            else:
                messages.error(request, 'Неверный email или пароль')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class SignUpView(View):

    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        logger.info(f"Loading sign up view")
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            cleaned_data = form.cleaned_data
            user = authenticate(email=cleaned_data['email'], password=cleaned_data['password1'])
            login(request, user)
            logger.info(f"User {cleaned_data['email']} signed up")
            asyncio.run(create_cart(user))
            asyncio.run(create_user_profile(user, cleaned_data.get('address'), cleaned_data.get('first_name'),
                                            cleaned_data.get('last_name'), cleaned_data.get('phone_number')))
            return HttpResponseRedirect(reverse('products:home'))
        messages.error(request, form.errors)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class SignOutView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        logger.info(f"User {request.user.email} logged out")
        logout(request)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ProfileView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user_profile = asyncio.run(get_user_profile(request.user))
        logger.info(f"Loading profile for {request.user.email}")
        return render(request, 'profile/user_profile.html', {'user_profile': user_profile})
