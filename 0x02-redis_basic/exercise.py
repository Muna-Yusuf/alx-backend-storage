#!/usr/bin/env python3

import redis
import uuid
from typing import Union, Callable, Optional
import functools


def count_calls(method: Callable) -> Callable:
    """Count the number of calls to a method"""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function to increment the call
           count and call the method."""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    def __init__(self):
        """initalize the cache and clear any existing data."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
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

    def get_str(self, key: str) -> Optional[str]:
        """Fetch data from Redis using the key
           and convert it to a string."""
        return self.get(key, lambda d: d.decode('uft-8'))

    def get_int(self, key: str) -> Optional[int]:
        """Retrieve data from Redis by key and convert it to an integer."""
        return self.get(key, lambda d: int(d))
