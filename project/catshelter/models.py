from django.db import models
# Create your models here.

class User(models.Model):
    userfullname = models.CharField(max_length=225, primary_key=True)
    useremail = models.CharField(max_length=225)
    userphone = models.IntegerField()
    status = models.CharField(max_length=225, default="Active")

class Login(models.Model):
    username = models.CharField(max_length=225, primary_key=True)
    password = models.CharField(max_length=225)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Cat(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    breed = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='cat_images/', null=True, blank=True)  # Add this field

class Image(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, related_name='images', null=True, blank=True)

class Admin(models.Model):
    admin_id = models.CharField(max_length=50, unique=True)
    admin_name = models.CharField(max_length=100)
    admin_contact = models.CharField(max_length=15)
    admin_email = models.EmailField(unique=True)

class AdminLogin(models.Model):
    admin = models.OneToOneField(Admin, on_delete=models.CASCADE, primary_key=True)
    password = models.CharField(max_length=225)

    def __str__(self):
        return self.admin.admin_name
    
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

