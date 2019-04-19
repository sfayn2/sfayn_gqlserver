from django.core.management.base import BaseCommand, CommandError
from cb.models import Product
from django.conf import settings
import json
import hashlib
import requests

class Command(BaseCommand):
    help = 'Pull Push Products'

    #def add_arguments(self, parser):
    #    parser.add_argument('poll_id', nargs='+', type=int)

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
        sku = None

        for p in prods:
            if not Product.objects.filter(sku=p["sku"]).exists():
                x = Product()
                for f in Product._meta.get_fields():
                    if f.name == "sku" and p.get(f.name):
                        sku = p.get(f.name)
                    if f.name != "id" and p.get(f.name):
                        setattr(x, f.name, p.get(f.name))
                x.save()
                self.stdout.write(self.style.SUCCESS("pullpush sku:{} -ok".format(sku)))

