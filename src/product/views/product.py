from django.views import generic, View
from rest_framework.generics import ListCreateAPIView
from django.db.models import Q
from product.models import *
from product.serializers import *

class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context

class ProductListView(generic.ListView):
    template_name = 'products/list.html'
    model = Product
    # paginate_by = 5
    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        product = Product.objects.all().values()
        newList = []
        for prod in product:
            newProduct = dict(prod)
            prod_variant = ProductVariant.objects.filter(product = prod['id']).all()
            for var in prod_variant:
                prodVarPrice = ProductVariantPrice.objects.prefetch_related('product_variant_one','product_variant_two','product_variant_three','product').filter( Q(product_variant_one=var.id) | Q(product_variant_two=var.id) |Q(product_variant_three=var.id)).all()
                # print(prodVarPrice)
            newProduct['variant'] = prod_variant
            # prod_variant_price = ProductVariantPrice.objects.filter(product_variant_one__in = prod_variant, product = prod['id']).all()
            # newProduct['variant_price'] = prod_variant_price
            # print(prod_variant_price)
            newList.append(newProduct)
        context['product'] = newList
        # context['product'] = product
        return context