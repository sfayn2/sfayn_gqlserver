from __future__ import annotations
from order_management import models as django_snapshots


class DjangoUserAuthorizationSnapshotSyncService:
    def __init__(self, user_auth_provider: UserAuthorizationSnapshotAbstract):
        self.user_auth_provider = user_auth_provider

    def sync(self):
        django_snapshots.UserAuthorizationSnapshot.objects.all().delete()

        users_auth = self.user_auth_provider.get_all_users_auth()
        for user_auth in users_auth:
            django_snapshots.UserAuthorizationSnapshot.objects.create(**user_auth.model_dump())