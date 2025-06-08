from graphene_django import DjangoObjectType
from .models import Product, Category, Tag, VariantItem

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = "__all__"

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"

class TagType(DjangoObjectType):
    class Meta:
        model = Tag
        fields = "__all__"

class VariantItemType(DjangoObjectType):
    class Meta:
        model = VariantItem
        fields = "__all__"