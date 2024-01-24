#!/usr/bin/env python3
"""
List all documents in collection
"""


def list_all(mongo_collection):
    """
    Prototype: list_all(mongo_collection)
    Return: empty list if no document in collection
    """
    docs = mongo_collection.find()
    return docs
