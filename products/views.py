from django.views.generic import ListView, DetailView, CreateView

from django.shortcuts import render
from django.utils.translation import gettext as _
from products.forms import CommentForm
from products.models import Product, Comment, Category


# Create your views here.
class ProductListView(ListView):
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.select_related('categories').filter(active=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.filter(parent=None)
        categories_with_children = {
            category: category.get_descendants() for category in categories
        }
        context['categories_with_children'] = categories_with_children
        return context



class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        product = Product.objects.get(pk=int(self.kwargs['pk']))
        obj.product = product
        return super().form_valid(form)
    
    
