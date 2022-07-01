from hashlib import md5
from logging import exception
from django.shortcuts import render,redirect
from django.http.response import JsonResponse,HttpResponse
from django.contrib import messages
from cryptography.fernet import Fernet
import requests
from user_app.decorators import login_is_required, logout_is_required
import re
# Create your views here.
key = Fernet.generate_key()
fernet = Fernet(key)


@logout_is_required
def Register(request):
    if request.method=='POST':
        post_data = {"full_name":request.POST.get('register_fullname'),
                    "username":request.POST.get('register_username'),
                    "password":request.POST.get('register_password')}
        try:
            url='http://127.0.0.1:9000/register_data'
            response = requests.post(url, data=post_data)
            
            if (response.json())['email_exist']:
                messages.success(request, 'Email already Exist', extra_tags='email_already')
                return redirect('/register')
            
            if (response.json())['success_message']:
                messages.success(request, 'Email has been sent, please confirm' , extra_tags='register')
                return redirect('/login')
            
            if (response.json())['error']:
                return HttpResponse('<h1> Server error</h1>')
    
        except:
            return HttpResponse('<h1> Server error</h1>')
        
    return render(request, 'register_page.html')

@logout_is_required
def HomePage(request):
    if(request.POST):
        post_data={'username':request.POST.get('login_username'),
                    'password':request.POST.get('login_password')}
        
        try:
            url='http://127.0.0.1:9000/check_user'
            response = requests.post(url, data=post_data)
            
            if (response.json())['no_account']:
                messages.success(request, 'NO account found', extra_tags='not_exist')
                return redirect('/')
            
            if (response.json())['no_confirm_email']:
                    messages.success(request, 'please confirm email first', extra_tags='confirm_email')
                    return redirect('/login')
        
            if (response.json())['success_message']:
                request.session['user_is_active']=True
                request.session['profile_name']=(response.json())['profile']
                request.session['user_key']=(response.json())['user_key_token']
                return redirect('/dashboard')
            
            if (response.json())['password_error']:
                messages.success(request, 'Wrong password', extra_tags='password_error')
                return redirect('/')
            
            if (response.json())['error']:
                return HttpResponse('<h1> Server error</h1>')
            
        except:
            return HttpResponse('<h1> Server error</h1>')
    return render(request, 'home_page.html')


@logout_is_required
def LogIn(request):
    if(request.POST):
        post_data={'username':request.POST.get('login_username'),
        'password':request.POST.get('login_password')}
        
        print(post_data)
        
        # try:
        #     url='http://127.0.0.1:9000/check_user'
        #     response = requests.post(url, data=post_data)

        #     if (response.json())['no_account']:
        #         messages.success(request, 'NO account found', extra_tags='not_exist')
        #         return redirect('/login')
            
        #     else:
        #         if (response.json())['no_confirm_email']:
        #             messages.success(request, 'please confirm email first', extra_tags='confirm_email')
        #             return redirect('/login')
                    
        #         if (response.json())['success_message']:
        #             request.session['user_is_active']=True
        #             request.session['profile_name']='kumar'
        #             request.session['user_key']=(response.json())['user_key_token']
        #             return redirect('/dashboard')
                
        #         if (response.json())['password_error']:
        #             messages.success(request, 'Wrong password', extra_tags='password_error')
        #             return redirect('/login')
                
        #         if (response.json())['error']:
        #             return HttpResponse('<h1> Server error</h1>')
                
        # except:
        #     return HttpResponse('<h1> Server error</h1>')
        
        

    return render(request, 'login_page.html')


def Forgot_password(request):
    return render(request, 'forgot_password.html')


@login_is_required
def Logout_user(request):
    session_keys = list(request.session.keys())
    for key in session_keys:
        del request.session[key]
    return redirect('/')
