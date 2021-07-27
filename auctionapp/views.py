from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User
# Create your views here.

def index(request):
    return render(request, 'index.html')

def register(request):
    return render(request, 'register.html')

def create_account(request):
    if request.method != 'POST': 
        return redirect('/')
    errors = User.objects.registration_validator(request.POST)
    if len(errors):
        for value in errors.values():
            messages.error(request, value)
        return redirect('/register')
    hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt(4)).decode()
    new_user = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = hashed_pw,
    )
    request.session['user_id'] = new_user.id 
    return redirect('/dashboard')

def login(request):
    if request.method != 'POST':
        return redirect('/')
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for value in errors.values():
            messages.error(request, value)
        return redirect('/')
    this_user = User.objects.filter(email=request.POST['email'])[0]  ##index 0 to find the ONE user
    if bcrypt.checkpw(request.POST['password'].encode(), this_user.password.encode()):
        request.session['user_id'] = this_user.id
        return redirect('/dashboard')
    messages.error(request, "Please enter a valid email and password")
    return redirect('/')

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user' : user,
    }
    return render(request, 'dashboard.html', context)
