from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse
# Create your models here.

class Category(MPTTModel):
    title = models.CharField(max_length=255, db_index=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    is_public = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, allow_unicode=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'




class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    sell_price = models.PositiveIntegerField()
    off_price = models.PositiveIntegerField(blank=True, null=True)
    offer = models.PositiveIntegerField(default=0 , blank=True, null=True)
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True , allow_unicode=True , blank=True, null=True)

    categories = models.ManyToManyField(Category , related_name='categories', blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.offer and self.offer > 0:
            discount = (self.offer / 100) * self.sell_price
            self.off_price = self.sell_price - discount
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product_detail' , args=[self.pk])

    @property
    def main_image(self):
        if self.images.exists():
            return self.images.first()
        else:
            return None



class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE ,related_name='images')
    image = models.ImageField(upload_to='products/')
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def delete(self , *args, **kwargs):
        super().delete(*args, **kwargs)
        for index , image in enumerate(self.product.images.all()):
            image.display_order = index
            image.save()