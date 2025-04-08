from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# License model
class License(models.Model):
    STATUS_CHOICES = (
        ('A', 'Active'),
        ('E', 'Expired'),
        ('P', 'Pending'),
    )
    type = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    issued_date = models.DateField()
    exp_date = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.type 

# Accountant model 
class Accountant(models.Model):
    TYPE_CHOICES = (
        ('I', 'Income'), 
        ('E', "Expense"),
    )
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    description = models.TextField()(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"self.get_type_display() - {self.name}"
    
    # Checklist model 
class Checklist(models.Model):
    STATUS_CHOICES = (
        ('R', 'Required'),
        ('P', 'In Progress'),
        ('C', 'Completed'),
    )
    title = models.CharField(max_length=100)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    date = models.DateField()
    notes = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title