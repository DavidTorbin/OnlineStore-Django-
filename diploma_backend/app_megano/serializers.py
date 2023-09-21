from rest_framework import serializers
from taggit.serializers import TagListSerializerField, TaggitSerializer
from taggit.models import Tag
from decimal import Decimal

from app_megano.models import Products, Category, ProductImages, Reviews, Specifications
from app_cart.serializers import TagSerializerField


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    date = serializers.DateTimeField(format='%a %b %d %Y %H:%M:%S %Z%z', input_formats=None)
    images = serializers.SerializerMethodField()
    tags = TagSerializerField()
    reviews = serializers.SerializerMethodField()
    rating = serializers.IntegerField(source='rate')

    class Meta:
        model = Products
        fields = ['id', 'category', 'price', 'count', 'date', 'title', 'description', 'href', 'freeDelivery',
                  'images', 'tags', 'reviews', 'rating']

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['category'] = ''.join(str(_) for _ in repr['category'])
        repr['price'] = Decimal(repr['price'])
        return repr

    def get_images(self, instance):
        images = (
            ProductImages.objects
            .filter(product=instance.id)
            .values_list('imageURL', flat=True)
        )
        return images

    def get_reviews(self, instance):
        return (
            Reviews.objects
            .filter(product=instance.id)
            .count()
        )


class SubcategorySerializer(serializers.ModelSerializer):
    href = serializers.CharField(source='get_absolute_url', read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'image', 'href']

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['id'] = str(repr['id'])
        return repr

    def get_image(self, obj):
        return {'src': obj.image_src.url, 'alt': obj.image_alt}


class CategorySerializer(serializers.ModelSerializer):
    href = serializers.CharField(source='get_absolute_url', read_only=True)
    subcategories = SubcategorySerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'image', 'href', 'subcategories']

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['id'] = str(repr['id'])
        return repr

    def get_image(self, obj):
        return {'src': obj.image_src.url, 'alt': obj.image_alt}


class TagsSerializer(TaggitSerializer):
    id = serializers.CharField(source='name', read_only=True)
    name = serializers.CharField(source='slug', read_only=True)

    class Meta:
        model = Tag
        fields = ['id', 'name']


class SpecificSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
    value = serializers.CharField()


class CatalogItemSerializer(ProductSerializer):
    reviews = serializers.SerializerMethodField()
    specification = SpecificSerializer()

    class Meta:
        model = Products
        fields = ['id', 'category', 'price', 'count', 'date', 'title', 'description', 'fullDescription',
                  'href', 'freeDelivery',  'images', 'tags', 'reviews', 'specification', 'rating']

    def get_reviews(self, instance):
        return (
            Reviews.objects
            .filter(product=instance.id)
            .values('author', 'email', 'text', 'rate', 'date')
            .order_by('date')
        )


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ['author', 'email', 'text', 'rate', 'date']

    def create(self, validated_data):
        return Reviews.objects.create(**validated_data)
