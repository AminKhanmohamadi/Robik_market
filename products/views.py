from django.views.generic import ListView, DetailView

from django.shortcuts import render

from products.models import Product


# Create your views here.
class ProductListView(ListView):
    queryset = Product.objects.filter(active=True)
    template_name = 'products/product_list.html'
    context_object_name = 'products'



class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = 'product'