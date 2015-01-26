# -*- coding: UTF-8 -*-

from django import forms
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.template import RequestContext
from django.contrib.messages.api import get_messages
from django.conf import settings
from jukebox.jukebox_core.models import Song, Genre

@login_required
def index(request):
        request.session.set_expiry(settings.SESSION_TTL)

        genres = Genre.objects.all()
        years = Song.objects.values("Year").distinct()
        years = years.exclude(Year=None).exclude(Year=0).order_by("Year")

        context = {
            "username": request.user.get_full_name(),
            "genres": genres,
            "years": years
        }
        context.update(csrf(request))
        return render_to_response('index.html', context)

def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    print password
    print username
    user = auth.authenticate(username=username, password=password)
    user.get_full_name()
    if user.is_authenticated():
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page.
        #return HttpResponseRedirect("/")
	return HttpResponseRedirect("success")
    else:
        # Show an error page
        return HttpResponseRedirect("login_failed")
    #if request.user.is_authenticated():
     #   return HttpResponseRedirect('index')
    #else:
    #    return render(request,
     #       'login.html',
      #      {
       #         "backends": settings.SOCIAL_AUTH_ENABLED_BACKENDS,
        #    }
       # )

def login_error(request):
    messages = get_messages(request)
    return render_to_response(
        'login_failed.html',
        {"error": messages},
        RequestContext(request)
    )

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

def language(request, language):
    from django.utils.translation import check_for_language
    from django.utils import translation

    response = HttpResponseRedirect("/")
    if language and check_for_language(language):
        if hasattr(request, "session"):
            request.session["django_language"] = language
        else:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
        translation.activate(language)

    return response


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {
        'form': form,
    })
