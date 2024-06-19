# web.py

import requests
import redis
from functools import wraps
import time

# Initialize Redis connection
redis_client = redis.Redis()

def count_calls(func):
    """Decorator to count the number of times a function is called."""
    @wraps(func)
    def wrapper(url, *args, **kwargs):
        key = f"count:{url}"
        redis_client.incr(key)
        return func(url, *args, **kwargs)
    return wrapper

def cache_result(timeout=10):
    """Decorator to cache function results in Redis with expiration."""
    def decorator(func):
        @wraps(func)
        def wrapper(url, *args, **kwargs):
            key = f"cache:{url}"
            cached_result = redis_client.get(key)
            if cached_result:
                return cached_result.decode('utf-8')
            result = func(url, *args, **kwargs)
            redis_client.setex(key, timeout, result)
            return result
        return wrapper
    return decorator

@count_calls
@cache_result()
def get_page(url: str) -> str:
    """Fetches the HTML content from a URL."""
    response = requests.get(url)
    return response.text

# Example usage
if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/https://example.com"
    html = get_page(url)
    print(html)
