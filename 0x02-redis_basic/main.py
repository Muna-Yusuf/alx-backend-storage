#!/usr/bin/env python3
""" Main file """
from exercise import Cache, replay

cache = Cache()

s1 = cache.store("first")
s2 = cache.store("secont")
s3 = cache.store("third")

replay(cache.store)
