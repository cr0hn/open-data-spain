import builtins

from django.conf import settings

import motor.motor_asyncio
from mongoengine import connect
from pymongo import MongoClient


def init_mongo():
    connect(host=settings.MONGO_DSN, user=settings.MONGO_USER, password=settings.MONGO_PASSWORD)


def mongo_connection() -> MongoClient:
    if getattr(builtins, "mongo_connection", None) is None:
        builtins.mongo_connection = MongoClient(settings.MONGO_DSN)

    return builtins.mongo_connection


def async_mongo_connection() -> motor.motor_asyncio.AsyncIOMotorClient:
    if getattr(builtins, "mongo_connection", None) is None:
        builtins.mongo_connection = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_DSN)

    return builtins.mongo_connection
