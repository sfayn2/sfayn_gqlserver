from __future__ import annotations
import pytz
import uuid
from typing import List
from datetime import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from django.contrib.auth.models import User, Permission
from ddd.order_management.domain import enums
from ddd.order_management.application import ports, dtos


class DjangoUserAuthorizationSnapshotProvider(ports.UserAuthorizationSnapshotAbstract):

    def get_all_users_auth(self) -> List[dtos.UserAuthorizationSnapshotDTO]:
        tracked_permissions = ("checkout_items", "place_order", "confirm_order", "change_vendorproductsnapshot")
        final_users_auth = []
        for user in User.objects.prefetch_related("user_permissions", "groups__permissions").all():
            all_perms = user.get_all_permissions()
            for perm in all_perms:
                if perm.startswith("order_management") and perm in tracked_permissions:
                    final_users_auth.append(
                        dtos.UserAuthorizationSnapshotDTO(
                            user_id=user.username,
                            permission_codename=perm.split(".")[1],
                            scope={"vendor_id": "v-123"},
                            is_active=user.is_active
                        )
                    )

        return final_users_auth

