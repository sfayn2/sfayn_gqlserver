
from django.contrib import admin
from django.db.models import Count
from graphql_relay import from_global_id
from django.db.models import Min, Max
from product.models import (
    ProductVariantItem,
    ProductCategory
)


def get_list_from_global_id(data):
    final_id = []
    for d in data:
        #need to convert graphene relay id to db id
        final_id.append(from_global_id(d)[1]) 
    return final_id


def get_price_min(id):
    qset = ProductVariantItem.objects.filter(parent_sn_id=id)
    return qset.aggregate(Min("price"))["price__min"]

def get_price_max(id):
    qset = ProductVariantItem.objects.filter(parent_sn_id=id)
    return qset.aggregate(Max("price"))["price__max"]

def get_l3_categories(category_id_list, level):

    category = ProductCategory
    category_qset = category.objects.all()
    l3_categories = None

    if  category.LevelChoices.LEVEL_1 == level:
        l2_categories = list(
            category_qset.filter(
                parent_id__in=category_id_list
            ).values_list('id', flat=True)
        )

        l3_categories = list(
            category_qset.filter(
                parent_id__in=l2_categories
            ).values_list('id', flat=True)
        )


    elif  category.LevelChoices.LEVEL_2 == level:
        l3_categories = list(
            category_qset.filter(
                parent_id__in=category_id_list
            ).values_list('id', flat=True)
        )


    return l3_categories


class CommonAdmin(admin.ModelAdmin):
    readonly_fields = ["created_by"]
    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if obj and not request.user.id == obj.created_by.id:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if obj and not request.user.id == obj.created_by.id:
            return False
        return True
