from django.shortcuts import render,redirect

def login_is_required(function=None ):
    def wrap(request, *args, **kwargs):
        if request.session.get('user_is_active', False):
            return function(request, *args, **kwargs)

        return redirect('/')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def logout_is_required(function=None ):
    def wrap(request, *args, **kwargs):
        if not request.session.get('user_is_active', False):
            return function(request, *args, **kwargs)

        return redirect('/dashboard')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap