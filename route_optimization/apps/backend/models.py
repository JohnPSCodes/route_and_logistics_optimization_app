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
