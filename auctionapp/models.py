from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# LOGIN PORTION
class UserManager(models.Manager):
    def validate(self, post_data):
        errors = {}
        if len(post_data['first_name']) < 2:
            errors['first_name'] = 'First Name must be at least 2 characters'

        if len(post_data['last_name']) < 2:
            errors['last_name'] = 'Last Name must be at least 2 characters'

        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = 'Invalid Email Address'
        
        email_check = self.filter(email=post_data['email'])
        if email_check:
            errors['email'] = "Email already in use"

        if len(post_data['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        
        if post_data['password'] != post_data['confirm']:
            errors['password'] = 'Passwords do not match'
        
        return errors
    
    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False

        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def register(self, post_data):
        pw = bcrypt.hashpw(post_data['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            first_name = post_data['first_name'],
            last_name = post_data['last_name'],
            email = post_data['email'],
            password = pw,
        )
    def updateme(self, post_data):
        errors = {}
        if len(post_data['first_name']) < 2:
            errors['first_name'] = 'First Name must be at least 2 characters'

        if len(post_data['last_name']) < 2:
            errors['last_name'] = 'Last Name must be at least 2 characters'

        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = 'Invalid Email Address'
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    objects = UserManager()