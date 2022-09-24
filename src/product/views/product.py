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
            prod_variant = ProductVariant.objects.select_related('variant','product').filter(product = prod['id']).all()
            prodVarPrice = ProductVariantPrice.objects.select_related('product_variant_one','product_variant_two','product_variant_three').filter( (Q(product_variant_one__in=prod_variant) & Q(product_variant_two__in=prod_variant) & Q(product_variant_three__in=prod_variant)) & Q(product = prod['id'])).all()
            newProduct['variant'] = prod_variant
            newProduct['variant_price'] = prodVarPrice
            newList.append(newProduct)
        context['product'] = newList
        # context['product'] = product
        return context