import pytest, os, json, time
from ddd.order_management.application import (
    commands,
    handlers,
    dtos
)
from ddd.order_management.domain import (
    services as domain_services,
)
from ddd.order_management.infrastructure import (
    repositories as infra_repo,
    access_control1,
    validations
)

@pytest.mark.django_db
def test_add_coupon_ok(
    fake_jwt_handler, 
    fake_access_control,
    domain_clock,
):

    access_control = access_control1.AccessControl1(
        jwt_handler=fake_jwt_handler()
    )

    command = commands.AddCouponCommand(
        order_id="ORD-1",
        coupon_code="EXPIRED-COUPON25"
    )

    user_ctx = fake_access_control().get_user_context(token="fake_jwt_token")

    response = handlers.handle_add_coupon(
        command=command,
        uow=infra_repo.DjangoOrderUnitOfWork(),
        access_control=fake_access_control(),
        coupon_validation=validations.DjangoCouponValidation(),
        user_ctx=user_ctx
    )


    assert response.success is False
    assert response.message == "Coupon code EXPIRED-COUPON25 no longer valid."
