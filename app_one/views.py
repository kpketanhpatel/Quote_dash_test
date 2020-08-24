from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

# Create your views here.

def index(request):
   return render(request, "home.html")

def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.validator(request.POST)
    print(errors)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/')
    else:
        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id
        # messages.success(request, "You have successfully registered!")
        return render(request, "quotes.html")
    return render(request, "quotes.html")

def login(request):
        # is this a post request?
    if request.method == 'POST':
        # let's use the post data to filter for users
        loggedin_user = User.objects.filter(email=request.POST['email'])
        # did we find a user?
        if len(loggedin_user) > 0:
            # storing User Object instead of Queryset containing user
            loggedin_user = loggedin_user[0]
            # does their submitted password match our password in the DB?
            if bcrypt.checkpw(request.POST['password'].encode(), loggedin_user.password.encode()):
                # storing user data in session
                request.session['name'] = loggedin_user.first_name
                request.session['user_id'] = loggedin_user.id
                # routing to success page
                return redirect('/quotes')
    # this wasn't a post request, let's redirect home
    return redirect('/')

def quotes(request):
    # Only need ONE context object, we can use multiple key value pairs
    # Corrected GET command to use user_id from session
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'quotes': Quote.objects.all(),
    }
    return render(request, "quotes.html", context)

def quotes_new(request):
    errors = Quote.objects.validator(request.POST)
    if errors:
        for key, values in errors.items():
            messages.error(request,values)
        return redirect('/quotes')

    else:
        Quote.objects.create(
        author = request.POST['author'],
        quote = request.POST['quote'],
        poster = User.objects.get(id=request.session['user_id'])
    )
    return redirect('/quotes')
def add_like(request, id):
    liked_message = Quote.objects.get(id=id)
    user_like = User.objects.get(id=request.session['user_id'])
    liked_message.likes_quote.add(user_like)  #there is an issue here.
    return redirect('/quotes')


def account_edit(request):
    context = {
        'user': User.objects.get(id=request.session['user_id']),
    }
    return render(request, "account_edit.html", context)