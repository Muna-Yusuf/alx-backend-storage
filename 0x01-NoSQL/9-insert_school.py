#!/usr/bin/env python3
""" Using pymongo for MongoDB Operations in Python. """
import pymongo


def insert_school(mongo_collection, **kwargs):
    """ Function inserts a new document in a collection based on kwargs. """
    data = mongo_collection.insert_one(kwargs)
    return data.inserted_id
