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
)

@pytest.mark.django_db
@pytest.mark.parametrize(
    "order_id, coupon_code, expected_success, expected_message",
    [
        ("ORD-1", "VALID2-COUPON25", True, "Order ORD-1 successfully add coupon."),
        ("ORD-1", "EXPIRED-COUPON25", False, "Coupon code EXPIRED-COUPON25 no longer valid."),
        ("ORD-1", "NOT-ACTIVE-COUPON25", False, "Coupon NOT-ACTIVE-COUPON25 is not offered by vendor vendor-1"),
        ("ORD-NONDRAFT-1", "VALID-COUPON25", False, "Only draft order can apply coupon."),

    ]
)
def test_add_coupon(
    fake_jwt_handler, 
    fake_access_control,
    domain_clock,
    order_id,
    coupon_code,
    expected_success,
    expected_message,
):

    access_control = access_control1.AccessControl1(
        jwt_handler=fake_jwt_handler()
    )

    command = commands.AddCouponCommand(
        order_id=order_id,
        coupon_code=coupon_code
    )

    user_ctx = fake_access_control().get_user_context(token="fake_jwt_token")

    response = handlers.handle_add_coupon(
        command=command,
        uow=infra_repo.DjangoOrderUnitOfWork(),
        access_control=fake_access_control(),
        coupon_validation=validations.DjangoCouponValidation(),
        user_ctx=user_ctx
    )


    assert response.success is expected_success
    assert response.message == expected_message
