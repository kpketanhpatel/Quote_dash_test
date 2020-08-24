from __future__ import unicode_literals
from django.db import models
import re
import bcrypt  
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 2:
            errors['first_name'] = "Your first name must be more than 2 characters!!"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Your last name must be more than 2 characters!!"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email must be valid format!!"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters!!"
        if postData['password'] != postData['conf_password']:
            errors['conf_password'] = "Password and confirm password do not match!!"
        return errors

    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False

        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())
    
    def register(self, form):
        pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            first_name = form['first_name'],
            last_name = form['last_name'],
            email = form['email'],
            password = pw,
        )


# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    objects = UserManager()

class Quote_Like(models.Model):
    poster = models.ForeignKey(User, related_name="user_likes", on_delete=models.CASCADE)  #confirm usage for related_name.
    likes = models.ManyToManyField(User, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class QuoteManager(models.Manager):
    def validator(self, form):
        errors = {}
        if len(form['author']) < 3:
            errors['first_name'] = "Your Author must be more than 3 characters!!"
        if len(form['quote']) < 10:
            errors['quote'] = "Your Quote must be more than 10 characters!!"
        return errors

class Quote(models.Model):
    author = models.CharField(max_length=255)
    quote = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    likes = models.ForeignKey(User, related_name="likes_quote", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()