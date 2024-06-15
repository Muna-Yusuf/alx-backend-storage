#!/usr/bin/env python3
"""Using pymongo for MongoDB Operations in Python."""


def top_students(mongo_collection):
    """Python function that returns all 
       students sorted by average score"""
    return mongo_collection.aggregate([
        {
            "$project":
                {
                    "name": "$name",
                    "averageScore": {"$avg": "$topics.score"}
                }
        },
        {
            "$sort":
                {
                    "averageScore": -1
                }
        }
    ])
