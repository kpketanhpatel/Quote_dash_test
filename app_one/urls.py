from django.urls import path     

from . import views
urlpatterns = [
    # Localhost 8000
    path('', views.index),
    #register the new user
    path('register', views.register),
    #login an existing user
    path('login', views.login),
    #bring user to all Quotes and ability to create new quotes
    path('quotes', views.quotes),
    #create a quote, and bring people back to the quote page.
    path('quotes_new', views.quotes_new),
    #edit account information for a particular user.
    path('account_edit', views.account_edit),
    #add like to a quote
    path('add_like/<int:id>', views.add_like)
]