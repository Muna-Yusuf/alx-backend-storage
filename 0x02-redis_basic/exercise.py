#!/usr/bin/env python3

import redis
import uuid
from typing import Union


class Cache:
    def __init__(self):
        """initalize the cache and clear any existing data."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store the data in Redis using a randomly
           generated key, then return the key."""

        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
