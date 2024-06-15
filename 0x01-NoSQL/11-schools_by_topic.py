#!/usr/bin/env python3
"""  Using pymongo for MongoDB Operations in Python. """
import pymongo


def schools_by_topic(mongo_collection, topic):
    """ Function returns the list of school having a specific topic."""
    return mongo_collection.find({"topics":  {"$in": [topic]}})
