from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Products, ProductImages, Specifications, Category, Subcategories, Reviews


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    pass


@admin.register(Specifications)
class SpecificationsAdmin(admin.ModelAdmin):
    pass


class SubcategoriesInline(admin.TabularInline):
    model = Subcategories


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_src', 'image_alt', 'preview', 'active', 'index_sort']
    readonly_fields = ('id', 'preview')
    inlines = [SubcategoriesInline, ]

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image_src.url}" style="max-height: 30px;">')


@admin.register(Subcategories)
class SubcategoriesAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'image_src', 'image_alt', 'active', 'preview', 'index_sort']
    readonly_fields = ('id', 'preview')

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image_src.url}" style="max-height: 30px;">')


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    ordering = ('product', '-date')
