from rest_framework import serializers

from app_megano.models import ProductImages, Reviews
from app_cart.models import CartItems
from app_cart.CartServices import CartService


class TagSerializerField(serializers.ListField):
    child = serializers.CharField()

    def to_representation(self, data):
        return list(data.values_list('name', flat=True))


class CartSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='item_id.id')
    date = serializers.DateTimeField(format='%a %b %d %Y %H:%M:%S %Z%z', input_formats=None)
    title = serializers.CharField(source='item_id.title')
    description = serializers.CharField(source='item_id.description')
    href = serializers.CharField(source='item_id.href')
    images = serializers.SerializerMethodField()
    tags = TagSerializerField(source='item_id.tags')
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = CartItems
        fields = ['id', 'category', 'price', 'count', 'date', 'title', 'description',
                  'href', 'freeDelivery', 'images', 'tags', 'reviews', 'rating']

    def get_images(self, obj):
        images = (
            ProductImages.objects
            .filter(product=obj.item_id)
            .values_list('imageURL', flat=True)
        )
        return images

    def get_reviews(self, obj):
        return (
            Reviews.objects
            .filter(product=obj.item_id)
            .count()
        )

