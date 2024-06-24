import random
import string

from django.db import models
from djstripe.models import Customer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from model_utils.models import TimeStampedModel, UUIDModel

from sdk.serializers import msgpack_dump, msgpack_load, MessagePackError


class UserRoles:
    ADMIN = 'admin'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Admin'),
        (USER, 'User'),
    ]


class ODSUser(AbstractUser):
    email = models.EmailField(unique=True, db_index=True, help_text='Email del usuario')
    role = models.CharField(max_length=100, choices=UserRoles.ROLES, default=UserRoles.USER, db_index=True, help_text='Rol del usuario')
    consumed_services = models.JSONField(default=dict, blank=True, null=True, help_text='Servicios consumidos por el usuario')
    avatar_url = models.URLField(blank=True, null=True, help_text='Avatar del usuario')

    stripe_customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True, related_name='user')

    def __init__(self, *args, **kwargs):
        self.cached_billing_name = kwargs.pop('cached_billing_name', None)

        super().__init__(*args, **kwargs)

    def serialize(self):
        return msgpack_dump({
            'id': self.id,
            'pk': self.pk,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_staff': self.is_staff,
            'is_active': self.is_active,
            'date_joined': self.date_joined.isoformat(),
            'role': self.role,
            'cached_billing_name': self.plan_name,
        })

    @classmethod
    def deserialize(cls, data: str) -> 'ODSUser' or None:
        try:
            json_data = msgpack_load(data)
        except MessagePackError:
            return None

        return cls(
            pk=json_data['pk'],
            id=json_data['id'],
            username=json_data['username'],
            first_name=json_data['first_name'],
            last_name=json_data['last_name'],
            email=json_data['email'],
            is_staff=json_data['is_staff'],
            is_active=json_data['is_active'],
            date_joined=json_data['date_joined'],
            role=json_data['role'],

            # Add cached fields
            cached_billing_name=json_data["cached_billing_name"],
        )

    @property
    def plan_name(self) -> str:
        if not self.cached_billing_name:
            self.cached_billing_name = self.billing_plan.name

        return self.cached_billing_name


# -------------------------------------------------------------------------
# API Keys
# -------------------------------------------------------------------------

class KeyStatus:
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    STATUS = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    ]


class APIKey(TimeStampedModel, UUIDModel, models.Model):
    name = models.CharField(max_length=255, help_text="El nombre de la clave", verbose_name='Nombre')
    key = models.CharField(max_length=100, unique=True, default=None, help_text="La clave de la API",
                           verbose_name='Key')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='api_keys')
    status = models.CharField(max_length=100, default=KeyStatus.ACTIVE, db_index=True, choices=(
        (KeyStatus.ACTIVE, 'Active'),
        (KeyStatus.INACTIVE, 'Inactive'),
    ))

    class Meta:
        ordering = ['-created']
        db_table = 'api_keys'
        verbose_name = 'API Key'
        verbose_name_plural = 'API Keys'

    @staticmethod
    def generate_random_api_keys() -> str:
        blocks = (4, 5, 12, 8, 4, 7, 4, 3)

        key = '-'.join(
            ''.join(random.choices(string.ascii_uppercase + string.digits, k=blocks[i]))
            for i in range(len(blocks))
        )

        return f"ODS_{key}"
