#!/usr/bin/env python3
""" Using pymongo for MongoDB Operations in Python. """
import pymongo


def update_topics(mongo_collection, name, topics):
    """function changes all topics of a school document based on the name."""
    return mongo_collection.update_many({
            "name": name
        },
        {
            "$set": {
                "topics": topics
            }
        })
