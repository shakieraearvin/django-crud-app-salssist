from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# License model
class License(models.Model):
    STATUS_CHOICES = (
        ('A', 'Active'),
        ('E', 'Expiring'),
        ('P', 'Pending'),
    )

    type = models.CharField(max_length=200)
    issue_date = models.DateField()
    exp_date = models.DateField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    document = models.FileField(upload_to='documents/', blank=True)
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='P'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.type} ({self.get_status_display()})"

# Accountant model 
class Accountant(models.Model):
    TYPE_CHOICES = (
        ('I', 'Income'),
        ('E', 'Expense'),
    )

    name = models.CharField(max_length=255)
    type = models.CharField(
        max_length=1,
        choices=TYPE_CHOICES,
        default='I'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    source = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    receipt = models.FileField(upload_to='receipts/', blank=True)  
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} | {self.get_type_display()} - ${self.amount} on {self.date}"

    
    # Checklist model 
class Checklist(models.Model):
    STATUS_CHOICES = (
        ('R', 'Required'),
        ('P', 'In Progress'),
        ('C', 'Completed'),
    )
    title = models.CharField(max_length=100)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='R')
    date = models.DateField()
    notes = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.get_status_display()} - {self.title}"