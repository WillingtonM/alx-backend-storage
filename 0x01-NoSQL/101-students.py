#!/usr/bin/env python3
"""
Module that return all students sorted by average score
Prototype: top_students(mongo_collection):
"""


def top_students(mongo_collection):
    """
    Module that return all students sorted by average score
    all students sorted by average score
    """
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
