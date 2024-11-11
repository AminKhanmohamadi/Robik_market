from django.contrib import admin


from mptt.admin import MPTTModelAdmin
from products.models import Product, ProductImage, Category, Comment


# Register your models here.
@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    mptt_level_indent = 20




class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class CommentInline(admin.TabularInline):
    model = Comment
    fields =['author', 'body' , 'stars' , 'active']
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'sell_price', 'off_price', 'offer', 'active']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductImageInline , CommentInline ]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['product' , 'author' , 'body' , 'stars'  , 'active']



