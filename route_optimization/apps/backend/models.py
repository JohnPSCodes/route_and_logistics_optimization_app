from django.db import models

# Create your models here.


class User(models.Model):
    # 'user_id' AUTO_INCREMENT + PRIMARY KEY
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  # Email with validation and unique
    password_hash = models.TextField()

    def __str__(self):
        return f"{self.name} < {self.email}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending','Pending'),
        ('assigned','Assigned'),
        ('delivered','Delivered'),
    ]

    customer_name = models.CharField(max_length=100)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=10,decimal_places=6)
    longitude = models.DecimalField(max_digits=10,decimal_places=6)
    priority = models.IntegerField(default=1)
    delivery_window_start = models.DateTimeField()
    delivery_window_end = models.DateTimeField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"