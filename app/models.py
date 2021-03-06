from django.db import models

# Create your models here.
#Servicios

class Services(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.IntegerField() 

    def __str__(self):
        return self.name

#python .\manage.py makemigrations



class Insumo (models.Model):

    name = models.CharField(max_length= 120)
    price = models.IntegerField()
    Image = models.ImageField(upload_to="insumos", null=True)
    Description =models.TextField()
    Stock = models.IntegerField()

    def __str__(self):
        return self.name


class Slider(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="sliders", null=True)

    def __str__(self):
        return self.name


class Gallery(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="gallery", null=True)

    def __str__(self):
        return self.name

class Mision(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name



class Vision(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

#options for class contact
options_query =[
    [0, "Request"],
    [1,"Demand"],
    [2,"Suggest"],

]

class Contacto(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    contact_type = models.IntegerField(choices=options_query)
    message = models.TextField()
    

    def __str__ (self):
        return self.name

class User(models.Model):
    username = models.CharField(max_length=50)
    frist_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    email = models.EmailField()
    password1 = models.CharField(max_length=15)
    password2 = models.CharField(max_length=15)

    def __str__ (self):
        return self.username



