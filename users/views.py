from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm, UserCreationForm
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ValuesUpdateForm

from social_django.models import UserSocialAuth
from .models import Profile

def register(request):
    createProfileIfNotExist(request)
    if checkValues(request) is False:
        return redirect('values')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    createProfileIfNotExist(request)
    if checkValues(request) is False:
        return redirect('values')

    user = request.user

    if Profile.objects.filter(user=user).count() < 1:
        Profile.objects.create(user=user).save()

    if user.has_usable_password() is False:
        return redirect ('password')

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    try:
        google_login = user.social_auth.get(provider='google-oauth2')
    except UserSocialAuth.DoesNotExist:
        google_login = None

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())


    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == "POST":
        userForm = UserUpdateForm(request.POST, instance=request.user)
        profileForm = ProfileUpdateForm(request.POST,
                                        request.FILES,
                                        instance=request.user.profile)

        passwordForm = PasswordForm(request.user, request.POST)
        valuesForm =  ValuesUpdateForm(request.POST, instance=request.user.profile)

        if userForm.is_valid() and profileForm.is_valid():
            userForm.save()
            profileForm.save()
            messages.success(request, "Your account has been updated!")
            return redirect('profile')
        elif passwordForm.is_valid():
            passwordForm.save()
            update_session_auth_hash(request, passwordForm.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        elif valuesForm.is_valid():
            valuesForm.save()
            messages.success(request, "Thanks for your input! We'll now be serving articles of exactly differing opinons, enjoy!")
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        userForm = UserUpdateForm(instance=request.user)
        profileForm = ProfileUpdateForm(instance=request.user.profile)
        passwordForm = PasswordForm(request.user)
        valuesForm = ValuesUpdateForm(instance=request.user)

    valueX = user.profile.economicScore * 2.5 + 250
    valueY = user.profile.socialScore * -2.5 + 250

    context = {
        'userForm': userForm,
        'profileForm': profileForm,
        'passwordForm': passwordForm,
        'valuesForm': valuesForm,
        'valueX': valueX,
        'valueY': valueY,
        'github_login': github_login,
        'google_login': google_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect,
    }

    return render(request, 'users/profile.html', context)

@login_required
def values (request):
    user = request.user

    if request.method == "POST":
        userForm = ValuesUpdateForm(request.POST, instance=request.user.profile)
        if userForm.is_valid():
            userForm.save()
            profile = request.user.profile
            profile.gaveValues = True
            profile.save()
            messages.success(request, "Thanks for your input! We'll now be serving articles of exactly differing opinons, enjoy!")
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        userForm = ValuesUpdateForm(instance=request.user.profile)

    context = {
        'form': userForm
    }

    return render(request, 'users/values.html', context)

@login_required
def password(request):
    createProfileIfNotExist(request)
    if checkValues(request) is False:
        return redirect('values')

    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'users/password.html', {'form': form})


def createProfileIfNotExist (request):
    if request.user.is_authenticated and Profile.objects.filter(user=request.user).count() < 1:
        Profile.objects.create(user=request.user).save()


def checkValues (request):
    if request.user.is_authenticated and Profile.objects.filter(user=request.user).count() is 1:
        profile = Profile.objects.filter(user=request.user).first()
        return profile.gaveValues
    return True
