from django.shortcuts import render
from Login_app.forms import UserForm, UserInfoForm

# Create your views here.

def index(request):
    dict={}
    return render(request, 'Login_app/index.html', context=dict)

def register(request):
    user_form = UserForm()
    user_info_form = UserInfoForm()
    dict = {'user_form': user_form, 'user_info_form':user_info_form}
    return render(request, 'Login_app/register.html', context=dict)
