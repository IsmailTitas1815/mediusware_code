from django.views import generic, View
from rest_framework.generics import ListCreateAPIView
from django.db.models import Q
from product.models import *
from product.serializers import *
from django_filters.views import FilterView

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
    # model = Product
    paginate_by = 3
    filterset_class = None
    def get_queryset(self):

        try:
            title = self.request.GET.get('title') if self.request.GET.get('title')!='' else None 
            variant = self.request.GET.get('variant') if self.request.GET.get('variant')!='' else None
            price_from = self.request.GET.get('price_from') if self.request.GET.get('price_from')!='' else None
            price_to = self.request.GET.get('price_to') if self.request.GET.get('price_to')!='' else None
            date = self.request.GET.get('date') if self.request.GET.get('date')!='' else None


            if title or variant or price_from or price_to or date:
                # print("title", title,"variant", variant,"price_from", price_from,"price_to", price_to,"date", date)
                # print('\n\n')
                product = product = Product.objects.select_related('productvariantprice', 'productvariant').filter(title__contains=title).all().values()

                # if title:
                #     product = Product.objects.select_related('productvariantprice', 'productvariant').filter(title__contains=title).all()

                # if date:
                #     print(product,"\n\n")
                #     product = product.objects.all()
                #     print("product 2",product)
            else:
                product = Product.objects.all().values()
            # product = Product.objects.all().values()
            newList = []
            for prod in product:
                newProduct = dict(prod)
                prod_variant = ProductVariant.objects.select_related('variant','product').filter(product = prod['id']).all()
                prodVarPrice = ProductVariantPrice.objects.select_related('product_variant_one','product_variant_two','product_variant_three').filter( (Q(product_variant_one__in=prod_variant) & Q(product_variant_two__in=prod_variant) & Q(product_variant_three__in=prod_variant)) & Q(product = prod['id'])).all()
                newProduct['variant'] = prod_variant
                newProduct['variant_price'] = prodVarPrice
                newList.append(newProduct)
            return newList
            # return self.filterset.qs.distinct()
        except:
            return []


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
        context['all_variant'] = Variant.objects.all()
        # context['product'] = product
        return context