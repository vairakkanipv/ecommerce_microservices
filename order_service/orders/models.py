from django.db import models

class Order(models.Model):
    STATUS =[
        ('pending','Pending'),
        ('confirmed','Confirmed'),
        ('failed','Failed'),
    ]
    product_id = models.IntegerField()
    quantity   = models.IntegerField()
    status     = models.CharField(max_length=20, choices=STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order #{seld.id}-> Product {self.product_id}- {self.status}"
    