from django.db import models
from django.contrib.auth.hashers import make_password
# Create your models here.

class User(models.Model):
    userfullname = models.CharField(max_length=225, primary_key=True)
    useremail = models.CharField(max_length=225)
    userphone = models.IntegerField()
    status = models.CharField(max_length=225, default="Active")

class Admin(models.Model):
    adminfullname = models.CharField(max_length=225, primary_key=True)
    adminemail = models.CharField(max_length=225)
    adminphone = models.IntegerField()
    status = models.CharField(max_length=225, default="Active")

class Login(models.Model):
    username = models.CharField(max_length=225, primary_key=True)
    password = models.CharField(max_length=225)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class AdminLogin(models.Model):
    username = models.CharField(max_length=225, primary_key=True)
    password = models.CharField(max_length=225)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)

class Cat(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    HEALTH_CHOICES = [
        ('Healthy', 'Healthy'),
        ('Sick', 'Sick'),
    ]

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    breed = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='cat_images/', null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    neuter = models.BooleanField(default=False)
    health_condition = models.CharField(max_length=50, choices=HEALTH_CHOICES, default='Healthy')

    def __str__(self):
        return self.name  # Add this field

class Image(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, related_name='images', null=True, blank=True)


class Report(models.Model):
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)
    report_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Report for {self.cat.name} at {self.created_at}'

class VolunteerDate(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.date}: {self.description}"
     
class VolunteerApplication(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    volunteer_date = models.ForeignKey(VolunteerDate, on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.volunteer_date.date}"

class Inventory(models.Model):
    item_name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.item_name

class Fund(models.Model):
    fund_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.item_name