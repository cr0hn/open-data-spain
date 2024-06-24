import hashlib

from django.db import models

from model_utils.models import TimeStampedModel, UUIDModel


class Cache(TimeStampedModel):
    key = models.CharField(max_length=512, primary_key=True)
    value = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.key

    class Meta:
        db_table = 'cache'
        verbose_name = 'Cache'
        verbose_name_plural = 'Caches'

    @classmethod
    def get(cls, key: str) -> str | None:
        if not key:
            return None

        _key = hashlib.sha256(key.encode()).hexdigest()

        try:
            return cls.objects.get(key=_key).value
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_json(cls, key: str) -> dict | None:
        if not key:
            return None

        _key = hashlib.sha256(key.encode()).hexdigest()

        try:
            v = cls.objects.get(key=_key).value

            if v is None:
                return {}
            else:
                return eval(v)
        except cls.DoesNotExist:
            return None

    @classmethod
    def set(cls, key, value):
        if not key:
            return None

        _key = hashlib.sha256(key.encode()).hexdigest()

        try:
            cache = cls.objects.get(key=_key)
            cache.value = value
            cache.save()
        except cls.DoesNotExist:
            cls.objects.create(key=_key, value=value)
