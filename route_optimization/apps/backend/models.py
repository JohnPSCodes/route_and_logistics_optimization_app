from django.db import models

# Create your models here.


class User(models.Model):
    # 'user_id' AUTO_INCREMENT + PRIMARY KEY
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  # Email with validation and unique
    password_hash = models.TextField()

    def __str__(self):
        return f"{self.name} < {self.email} >"

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

class Route(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    name = models.CharField(max_length=100)
    planned_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')

    driver = models.ForeignKey(
        "Driver", 
        on_delete=models.SET_NULL,  
        null=True, blank=True,      
        related_name="routes"   
    )

    def __str__(self):
        return f"{self.name} ({self.planned_date})"
    
class Stop(models.Model):
    route = models.ForeignKey(
        'Route',
        on_delete=models.CASCADE,
        related_name='stops'
    )
    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
        related_name='stops'
    )
    stop_order = models.IntegerField()
    estimated_arrival = models.DateTimeField()
    delivered = models.BooleanField(default=False)
    delivery_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Stop {self.stop_order} - Route: {self.route.name} - Order ID: {self.order.id}"

class Driver(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="driver_profile")
    license_number = models.CharField(max_length=100,blank=True,null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.name