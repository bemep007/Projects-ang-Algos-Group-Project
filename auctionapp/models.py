from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# LOGIN PORTION
class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 1:
            errors['first_name'] = "First name is required"

        if len(postData['last_name']) < 1:
            errors['last_name'] = "Last name is required"

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email does not match format"

        if len(postData['password']) < 4:
            errors['password'] = "Password must be at least 4 characters long"

        if postData['password'] != postData['confirm_password']:
            errors['mismatch'] = "Both entered passwords do not match"

        existing_users = User.objects.filter(email=postData['email'])
        if len(existing_users) != 0:
            errors['existing'] = "That Email is already registered"

        return errors

        
    def login_validator(self, postData):
        errors = {}
        if len(postData['email']) < 1:
            errors['email'] = "Email is a required field"
        if len(postData['password']) < 1: 
            errors['password'] = "Enter password to login"
        return errors
    
    
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class ItemManager(models.Manager):
    def item_validator(self, postData):
        errors = {}

        if len(postData['item_brand']) < 1:
            errors['item_brand'] = "The brand name cannot be empty."
        if len(postData['product_name']) < 1:
            errors['product_name'] = "The product name cannot be empty."
        if len(postData['item_price']) < 1:
            errors['item_price'] = "The price cannot be empty."
        if len(postData['item_description']) < 1:
            errors['item_description'] = "The description name cannot be empty."
        if len(postData['contact_info']) < 1:
            errors['contact_info'] = "The contact information cannot be empty."

        # if postData['price'] == 0:
        #     errors['price'] = "The price cannot be $0."

        if len(postData['item_brand']) < 2:
            errors['item_brand'] = "The brand name must be at least 2 characters long."
        if len(postData['product_name']) < 8:
            errors['product_name'] = "Product name must be at least 8 characters long."
        if len(postData['item_description']) >50:
            errors['item_description'] = "The description must be less than 50 characters long."

        return errors
    def updateme(self, postData):
        errors = {}
        if len(postData['item_brand']) < 1:
            errors['item_brand'] = "The brand name cannot be empty."
        if len(postData['product_name']) < 1:
            errors['product_name'] = "The product name cannot be empty."
        if len(postData['item_price']) < 1:
            errors['item_price'] = "The price cannot be empty."
        if len(postData['item_description']) < 1:
            errors['item_description'] = "The description name cannot be empty."
        if len(postData['contact_info']) < 1:
            errors['contact_info'] = "The contact information cannot be empty."

        # if postData['price'] == 0:
        #     errors['price'] = "The price cannot be $0."

        if len(postData['item_brand']) < 2:
            errors['item_brand'] = "The brand name must be at least 2 characters long."
        if len(postData['product_name']) < 8:
            errors['product_name'] = "Product name must be at least 8 characters long."
        if len(postData['item_description']) >50:
            errors['item_description'] = "The description must be less than 50 characters long."


class Item(models.Model):
    product_name = models.CharField(max_length=45)
    item_description = models.CharField(max_length=50)
    item_price = models.IntegerField(max_length=8)
    contact_info = models.CharField(max_length=255)
    item_brand = models.CharField(max_length=45)
    owner = models.ForeignKey(User, related_name="has_created_item", on_delete=models.CASCADE)
    sold = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = ItemManager()