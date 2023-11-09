from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Offermodel(models.Model):
    OFFER_CHOICES = (
        ('money', 'Money'),
        ('percentage', 'Percentage'),
        ('fixed_amount', 'Fixed Amount'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    offer_type =models.CharField(max_length=50,choices=OFFER_CHOICES,null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=False)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    additional_info = models.TextField(blank=True)