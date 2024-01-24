#!/usr/bin/env python3
"""
Insert document in Python
"""
import pymongo


def insert_school(mongo_collection, **kwargs):
    """
    insert documents into collection
    """
    dt = mongo_collection.insert_one(kwargs)
    return dt.inserted_id
