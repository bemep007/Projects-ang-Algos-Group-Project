from django.shortcuts import render, redirect
from django.contrib import messages, auth
from .models import User, Item
# Create your views here.

def index(request):
    return render(request, 'index.html')


# My Account Pages
def my_account(request, user_id):
    context = {
        'user': User.objects.get(id=user_id),
        'all_items': Item.objects.get(owner=user_id),
    }
    return render(request, 'my_account.html', context)

def update_account(request, user_id):
    update_this_user=User.objects.get(id=user_id)
    errors = User.objects.updateme(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect(f'/my_account/{user_id}')
    else:
        update_this_user.first_name = request.POST['first_name']
        update_this_user.last_name = request.POST['last_name']
        update_this_user.email = request.POST['email']
        update_this_user.save()
    return redirect(f'/my_account/{user_id}')