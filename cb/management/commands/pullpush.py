from django.core.management.base import BaseCommand, CommandError
from cb.models import Product, ProductWarehouse, ProductOriginalImg, ProductDescImg
from django.conf import settings
import json
import hashlib
import requests

class Command(BaseCommand):
    help = 'Pull Push Products'

    #def add_arguments(self, parser):
    #    parser.add_argument('poll_id', nargs='+', type=int)

    UNWANTED_KEYS = ("original_img", "desc_img", "map", "warehouse_list")

    def remove_unwanted_keys(self, items=None):
        for k in self.UNWANTED_KEYS:
            if k in items:
                items.pop(k)
        return items


    def handle(self, *args, **options):

        self.stdout.write(self.style.SUCCESS('pullpush executing...'))

        #get token first
        login_url = "{}/v2/user/login".format(settings.CB_DOMAIN)
        json_data = json.dumps(settings.CB_ADD_REQ_TOKEN)
        signature = hashlib.md5((json_data + settings.CB_CLIENT_SECRET).encode('utf')).hexdigest()
        response = requests.post(login_url, data={'signature': signature, 'data': json_data})
        token = json.loads(response.text)['msg']['token']
        #get token first

        #get goods sn
        inventory_url = "{}/v2/user/inventory".format(settings.CB_DOMAIN)
        data = { "token": token, "type": 1, "per_page": 50, "page_number": 1 } 
        res = requests.post(inventory_url, data)
        goods_sn = []
        for g in json.loads(res.text)['msg']['page_result']:
            goods_sn.append(g['goods_sn'])
        #goods_sn = ["175919601"]
        #get goods sn

        #get product info
        prod_url = "{}/v2/product/index".format(settings.CB_DOMAIN)
        res = requests.post(prod_url, {'token': token, 'goods_sn': json.dumps(goods_sn)} )

        prods = json.loads(res.text)['msg']

        for p in prods:

            #{'status': 0, 'msg': 'Product unavailable or out of circulation', 'errcode': 15015}
            if p.get("errcode"): #skip when theres error in API results
                continue #next item if this have error

            warehouse_list = None
            if p.get("warehouse_list"):
                warehouse_list = p.get("warehouse_list")
            
            original_img = None
            if p.get("original_img"):
                original_img = p.get("original_img")
            
            desc_img = None
            if p.get("desc_img"):
                desc_img = p.get("desc_img")

            sku_items = self.remove_unwanted_keys(p) #cleanup unwanted keys. it will cause error in get or create

            sku_obj, sku_created = Product.objects.update_or_create(**sku_items)
            if sku_created:
                self.stdout.write(self.style.SUCCESS("newly created sku:{} title:{}".format(sku_obj.sku, sku_obj.title)))
            else:
                self.stdout.write(self.style.SUCCESS("updated sku:{} title:{}".format(sku_obj.sku, sku_obj.title)))


            if warehouse_list:
                for wl in warehouse_list.values(): #multiple list of dict
                    w_items = {}
                    w_items["product_id"] = sku_obj.sku
                    w_items["defaults"] = wl
                    w_obj, w_created = ProductWarehouse.objects.update_or_create(**w_items)
                    if w_created:
                        self.stdout.write(self.style.SUCCESS("newly created warehouse:{}".format(w_obj.warehouse)))
                    else:
                        self.stdout.write(self.style.SUCCESS("updated warehouse:{}".format(w_obj.warehouse)))


            if original_img:
                for oi in original_img:
                    oi_items = {}
                    oi_items["product_id"] = sku_obj.sku
                    oi_items["defaults"] = {}
                    oi_items["defaults"]["original_img"] = oi
                    oi_obj, oi_created = ProductOriginalImg.objects.update_or_create(**oi_items)
                    if oi_created:
                        self.stdout.write(self.style.SUCCESS("newly created original img:{}".format(oi_obj.original_img)))
                    else:
                        self.stdout.write(self.style.SUCCESS("updated original img:{}".format(oi_obj.original_img)))


            if desc_img:
                for di in desc_img:
                    di_items = {}
                    di_items["product_id"] = sku_obj.sku
                    di_items["defaults"] = {}
                    di_items["defaults"]["desc_img"] = di
                    di_obj, di_created = ProductDescImg.objects.update_or_create(**di_items)
                    if di_created:
                        self.stdout.write(self.style.SUCCESS("newly created desc img:{}".format(di_obj.desc_img)))
                    else:
                        self.stdout.write(self.style.SUCCESS("updated desc img:{}".format(di_obj.desc_img)))



