from django.contrib import admin
from .models import *
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'description','sku','created_at','updated_at')
    readonly_fields = ('created_at','updated_at')
    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)
# admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Variant)
admin.site.register(ProductVariant)
admin.site.register(ProductVariantPrice)