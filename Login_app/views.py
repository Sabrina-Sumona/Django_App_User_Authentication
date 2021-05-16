from django.shortcuts import render
from Login_app.forms import UserForm, UserInfoForm
from Login_app.models import UserInfo
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.

def index(request):
    dict={}
    if request.user.is_authenticated:
        current_user = request.user

        # print in console
        # print(current_user.username)
        # print(current_user.email)

        user_id = current_user.id
        # pk = primary key
        user_basic_info = User.objects.get(pk=user_id)
        # to retrive the info of related tables (here 1-to-1)
        # here 2 '_' is used to separate 2 column names of user & user_info
        user_more_info = UserInfo.objects.get(user__pk=user_id)
        dict = {'user_basic_info': user_basic_info,
                'user_more_info': user_more_info}
    return render(request, 'Login_app/index.html', context=dict)

# we cant rename this as just login because it will crash with existing module
def login_page(request):
    return render(request, 'Login_app/login.html', context={})

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        user_info_form = UserInfoForm(data=request.POST)

        if user_form.is_valid() and user_info_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            user_info = user_info_form.save(commit=False)
            # making one-to-one relationship between two tables
            user_info.user = user

            # for any kind of file inputs do this
            if 'profile_pic' in request.FILES:
                user_info.profile_pic = request.FILES['profile_pic']

            user_info.save()
            registered = True

    else:
        user_form = UserForm()
        user_info_form = UserInfoForm()
    dict = {'user_form': user_form, 'user_info_form':user_info_form,'registered':registered}
    return render(request, 'Login_app/register.html', context=dict)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                # check login or not
                login(request, user)

                # if we use this the page view & url both will redirect
                return HttpResponseRedirect(reverse('Login_app:index'))

                # if we use these the page view will redirect but the url will remain the same
                # return render(request, 'Login_app/index.html', context=dict)
                # return index(request)

            else:
                return HttpResponse("Account is not active!!")
        else:
            return HttpResponse("Login Details are Wrong!")
    else:
        # return render(request, 'Login_app/login.html', context={})
        return HttpResponseRedirect(reverse('Login_app:login'))

# this decorator checks login or not
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Login_app:index'))
