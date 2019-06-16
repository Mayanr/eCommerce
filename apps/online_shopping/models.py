from __future__ import unicode_literals
from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class CategoryManager(models.Manager):
    def basic_validator(self, postData):
        pass

class ProdManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 2:
            errors["name"] = "First Name should be at least 2 letters (and only letters)"
        return errors

class Additional_ImgManager(models.Manager):
    def basic_validator(self, postData):
        pass

class OrderManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['ship_fname']) < 2 or not str.isalpha(postData['ship_fname']):
            errors["ship_fname"] = "Shipping first name should be at least 2 letters (and only letters)."
        if len(postData['ship_lname']) < 2 or not str.isalpha(postData['ship_lname']):
            errors["ship_lname"] = "Shipping last name should be at least 2 letters (and only letters)."
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = 'Please enter a valid email'
        if len(postData['ship_address']) < 2:
            errors["ship_address"] = "Shipping address should be at least 2 characters."
        
        if len(postData['ship_city']) < 2 or not str.isalpha(postData['ship_lname']):
            errors["ship_city"] = "Shipping city name should be at least 2 letters (and only letters)."
        if len(postData['ship_state']) < 2 or not str.isalpha(postData['ship_lname']):
            errors["ship_state"] = "Shipping state should be at least 2 letters (and only letters)."
        if len(postData['ship_zip']) < 4 or len(postData['ship_zip']) > 6 or str.isalpha(postData['ship_zip']):
            errors["ship_zip"] = "Shipping zip code should be at least 5 digits."
        # if len(postData['ship_address2']) < 6:
        #     errors["ship_address2"] = "Zip code should be at least 5 numbers."


        if len(postData['bill_fname']) < 2 or not str.isalpha(postData['bill_fname']):
            errors["bill_fname"] = "Billing first name should be at least 2 letters (and only letters)."
        if len(postData['bill_lname']) < 2 or not str.isalpha(postData['bill_lname']):
            errors["bill_lname"] = "Billing last name should be at least 2 letters (and only letters)"
        if len(postData['bill_address']) < 2:
            errors["bill_address"] = "Billing address should be at least 2 letters (and only letters)."
        # if len(postData['bill_city']) < 2 or not str.isalpha(postData['bill_city']):
        #     errors["bill_city"] = "Billing city name should be at least 2 letters (and only letters)."
        if len(postData['bill_state']) < 2 or not str.isalpha(postData['bill_state']):
            errors["bill_state"] = "Billing state should be at least 2 letters (and only letters)."
        if len(postData['bill_zip']) < 4 or len(postData['bill_zip']) > 6 or str.isalpha(postData['bill_zip']):
            errors["bill_zip"] = "Billing zip code should be at least 5 digits."
        return errors

class Order_ItemManager(models.Manager):
    def basic_validator(self, postData):
        pass

class StatusManager(models.Manager):
    def basic_validator(self, postData):
        pass

class Category(models.Model):
    title = models.CharField(max_length=245)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CategoryManager()
    # prod_in_category ... from Prod class

class Prod(models.Model):
    name = models.CharField(max_length=245)
    desc = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    cat = models.ForeignKey(Category, related_name="prod_in_category")
    main_img = models.TextField()
    count = models.IntegerField()
    sold = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProdManager()
    # more_img ... from Additional_Img class
    # included_in_order ...from Order_Item 

class Additional_Img(models.Model):
    image_file = models.TextField()
    for_prod= models.ForeignKey(Prod, related_name="more_img")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Additional_ImgManager()

class Status(models.Model):
    progress = models.CharField(max_length=245)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = StatusManager()
    # status_label ... from Order class

class Order(models.Model):
    b_fname = models.CharField(max_length=245)
    b_lname = models.CharField(max_length=245)
    b_address = models.TextField()
    b_address2 = models.TextField()
    b_city = models.CharField(max_length=245)
    b_state = models.CharField(max_length=2)
    b_zip = models.IntegerField()
    sh_fname = models.CharField(max_length=245)
    sh_lname = models.CharField(max_length=245)
    sh_address = models.TextField()
    sh_address2 = models.TextField()
    sh_city = models.CharField(max_length=245)
    sh_state = models.CharField(max_length=2)
    sh_zip = models.IntegerField()
    email = models.CharField(max_length=245)
    total_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    status = models.ForeignKey(Status, related_name="status_label")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = OrderManager()
    # items_forthis_shopper ....from Order_Item class

class Order_Item(models.Model):
    includes_prod= models.ForeignKey(Prod, related_name="included_in_order")
    quant = models.IntegerField()
    cost = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    belongs_to_shopper= models.ForeignKey(Order, related_name="items_forthis_shopper")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Order_ItemManager()