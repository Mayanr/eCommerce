from __future__ import unicode_literals
from django.db import models

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
        pass

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
    main_img = models.ImageField(upload_to='images/')
    count = models.IntegerField()
    sold = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProdManager()
    # more_img ... from Additional_Img class
    # included_in_order ...from Order_Item 

class Additional_Img(models.Model):
    image_file = models.ImageField(upload_to='images/')
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
    status = models.ForeignKey(Status, related_name="status_label")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = OrderManager()
    # items_forthis_shopper ....from Order_Item class

class Order_Item(models.Model):
    includes_prod= models.ForeignKey(Prod, related_name="included_in_order")
    quant = models.IntegerField()
    belongs_to_shopper= models.ForeignKey(Order, related_name="items_forthis_shopper")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Order_ItemManager()