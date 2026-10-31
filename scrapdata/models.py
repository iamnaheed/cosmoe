from django.db import models

class ProductRecord(models.Model):
    title = models.CharField(max_length=255)
    rating = models.CharField(max_length=50)
    review_count = models.CharField(max_length=50)
    sold_count = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    image_src = models.CharField(max_length=255)
    addtocart_href = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Create your models here.
