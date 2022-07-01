from django.shortcuts import render
from user_app.decorators import login_is_required

# Create your views here.
@login_is_required
def Dashboard(request):
    print(request.session['user_key'])
    return render(request, 'dashboard.html')