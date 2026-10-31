from django.contrib import admin
from .models import ProductRecord

class ProductRecordAdmin(admin.ModelAdmin):
    list_display = ('title', 'rating', 'review_count', 'sold_count', 'price', 'created_at')
    search_fields = ['title', 'rating', 'review_count', 'sold_count', 'price']
    list_filter = ['created_at']

admin.site.register(ProductRecord, ProductRecordAdmin)
