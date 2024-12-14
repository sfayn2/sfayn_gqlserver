from ddd.product_catalog.app import unit_of_work

def get_product():
    with unit_of_work.DjangoUnitOfWork() as uow:
        domain_product = uow.product.get(product_id="e3bf4346-864a-4875-8ef3-ed3909f49e48")
        domain_product.pending_review()

        uow.product.save(domain_product)
        uow.commit()



