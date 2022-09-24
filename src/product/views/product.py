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
            prod_var_and_price = []
            for var in prod_variant:
                prodVarPrice = ProductVariantPrice.objects.filter( (Q(product_variant_one=var.id) | Q(product_variant_two=var.id) | Q(product_variant_three=var.id)) & Q(product = prod['id'])).first()
                li = [var, prodVarPrice]
                prod_var_and_price.append(li)
            newProduct['variant'] = prod_var_and_price
            # print("tup[0]",newProduct['variant'][1][0])
            # print(prod['id'], newProduct['variant'])
            newList.append(newProduct)
        context['product'] = newList
        # context['product'] = product
        return context