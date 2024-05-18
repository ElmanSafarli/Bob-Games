from django.contrib import admin
from .models import Category, Subcategory, Product, HomePage
from import_export.admin import ImportExportModelAdmin

@admin.register(Product)
class userdat(ImportExportModelAdmin):
    list_display = ('title', 'price', 'year', 'genre', 'language', 'is_in_stock', 'subcategory')
    search_fields = ('title', 'genre', 'language')
    list_filter = ('is_in_stock', 'subcategory__category', 'subcategory')
    list_select_related = ('subcategory',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'image')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('title', 'price', 'year', 'genre', 'language', 'is_in_stock', 'subcategory')
#     search_fields = ('title', 'genre', 'language')
#     list_filter = ('is_in_stock', 'subcategory__category', 'subcategory')
#     list_select_related = ('subcategory',)

@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ('id',)

