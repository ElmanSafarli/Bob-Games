from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='category_images/')

    def __str__(self):
        return self.name
class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return f"{self.category} - {self.name}"

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    year = models.PositiveIntegerField()
    genre = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    text1 = models.TextField()
    text2 = models.TextField()
    text3 = models.TextField()
    image1 = models.ImageField(upload_to='product_images/')
    image2 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image4 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    is_in_stock = models.BooleanField(default=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='products')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class HomePage(models.Model):
    image1 = models.ImageField(upload_to='home_page_images/')
    image2 = models.ImageField(upload_to='home_page_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='home_page_images/', blank=True, null=True)
    image4 = models.ImageField(upload_to='home_page_images/', blank=True, null=True)
    image5 = models.ImageField(upload_to='home_page_images/', blank=True, null=True)
    image6 = models.ImageField(upload_to='home_page_images/', blank=True, null=True)
    image7 = models.ImageField(upload_to='home_page_images/', blank=True, null=True)
    image8 = models.ImageField(upload_to='home_page_images/', blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return f"Home Page - {self.id}"


class Cart(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=40, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)