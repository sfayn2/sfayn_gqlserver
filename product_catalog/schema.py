import graphene
from .types import ProductType, CategoryType, TagType, VariantItemType
from .models import Product, Category, Tag, VariantItem

class Query(graphene.ObjectType):
    all_products = graphene.List(ProductType)
    all_categories = graphene.List(CategoryType)
    all_tags = graphene.List(TagType)
    all_variants = graphene.List(VariantItemType)
    product_by_id = graphene.Field(ProductType, id=graphene.ID(required=True))

    def resolve_all_products(root, info):
        return Product.objects.all()

    def resolve_all_categories(root, info):
        return Category.objects.all()

    def resolve_all_tags(root, info):
        return Tag.objects.all()

    def resolve_all_variants(roo, info):
        return VariantItem.objects.all()

    def resolve_product_by_id(root, info, id):
        try:
            return Product.objects.get(pk=id)
        except Product.DoesNotExist:
            return None

schema = graphene.Schema(query=Query)