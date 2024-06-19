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

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[
            str, bytes, int, float, None]:
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key:str) -> Optional[str]:
        """Fetch data from Redis using the key 
           and convert it to a string."""
        return self.get(key, lambda d: d.decode('uft-8'))

    def get_int(self, key: str) -> Optional[int]:
        """Retrieve data from Redis by key and convert it to an integer."""
        return self.get(key, lambda d: int(d))
