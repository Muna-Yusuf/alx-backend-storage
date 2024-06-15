#!/usr/bin/env python3
""" Using pymongo for MongoDB Operations in Python. """
import pymongo


def list_all(mongo_collection):
    """ Function that lists all documents in a collection. """

    docs = mongo_collection.find()
    return docs if docs else []
