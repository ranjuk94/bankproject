from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_banker = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username


from django.db import models

class Customer(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name='customer_profile')
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    account_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    dob = models.DateField()
    age = models.IntegerField()
    pan_number = models.CharField(max_length=10)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    aadhar_number = models.CharField(max_length=12)
    initial_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return f"{self.name} ({self.account_number})"


from django.db import models


class Transaction(models.Model):
    customer = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE,
        related_name='transactions'
    )  # Links to the Customer model

    branch = models.CharField(max_length=100)
    bank = models.CharField(max_length=100, default='')
    ifsc = models.CharField(max_length=11, default='')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    details = models.TextField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction for {self.customer.name} on {self.date} at {self.time}"