from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Expense(models.Model):
    CATEGORY_CHOICES=[
        ('Food','Food'),
        ('Bill','Bill'),
        ('Fuel','Fuel'),
    ]
    
    PAYMENT_CHOICES=[
        ('UPI', 'UPI'),
        ('Card', 'Card'),
    ]

    title=models.CharField(max_length=100)
    amount=models.DecimalField(max_digits=8, decimal_places=2)
    owner=models.ForeignKey(User, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    category=models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="Food")
    payment=models.CharField(max_length=20, choices=PAYMENT_CHOICES, default="UPI")

    def __str__(self):
        return f"{self.title} - {self.amount}"
