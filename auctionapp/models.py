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

# Bid Class - Item can have many bids but bid can be placed only on one item
# class Bid(models.Model):    
#     item_bid = models.IntegerField(max_length=8)
#     item_bid_on = models.ForeignKey(Item, related_name="has_a_bid", on_delete=models.CASCADE)
#     bidder = models.ForeignKey(User, related_name="has_bidded_onthis_item", on_delete=models.CASCADE)
#     created_at = models.DateField(auto_now_add=True)
#     updated_at = models.DateField(auto_now=True)

