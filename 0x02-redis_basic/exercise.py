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


def call_history(method: Callable) -> Callable:
    """Store the history of inputs and outputs for a function"""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function to log the input and output of the method."""
        key = method.__qualname__
        input_key = f"{key}:inputs"
        output_key = f"{key}:outputs"

        self._redis.rpush(input_key, str(args))

        result = method(self, *args, **kwargs)

        self._redis.rpush(output_key, str(result))

        return result
    return wrapper


def replay(method: Callable) -> None:
    """Display the history of calls of a particular function."""
    key = method.__qualname__
    input_key = f"{key}:inputs"
    output_key = f"{key}:outputs"
    inputs = method.__self__._redis.lrange(input_key, 0, -1)
    outputs = method.__self__._redis.lrange(output_key, 0, -1)

    print(f"{key} was called {len(inputs)} times:")
    for input_str, output_str in zip(inputs, outputs):
        decoded_input = input_str.decode('utf-8')
        decoded_output = output_str.decode('utf-8')
        print(f"{key}(*{decoded_input}) -> {decoded_output}")


class Cache:
    def __init__(self):
        """initalize the cache and clear any existing data."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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
