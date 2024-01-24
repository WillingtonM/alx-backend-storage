#!/usr/bin/env python3
"""
Module that returns list of school having a specific topic
"""


def schools_by_topic(mongo_collection, topic):
    """
    Returns list of schools having specific topic
    mongo_collection: will be pymongo collection object
    topic: will be topic searched
    """
    return mongo_collection.find({"topics": topic})
