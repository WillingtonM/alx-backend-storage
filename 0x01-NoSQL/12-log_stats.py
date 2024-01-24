#!/usr/bin/env python3
"""
Module that Provides some stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]


def log_stats(mongo_collection, option=None):
    """
    function provides some stats about Nginx logs stored in MongoDB
    """
    items = {}
    if option:
        val = mongo_collection.count_documents(
            {"method": {"$regex": option}})
        print(f"\tmethod {option}: {val}")
        return

    res = mongo_collection.count_documents(items)
    print(f"{res} logs")
    print("Methods:")
    for mthod in METHODS:
        log_stats(nginx_collection, mthod)
    state_check = mongo_collection.count_documents({"path": "/status"})
    print(f"{state_check} status check")


if __name__ == "__main__":
    nginx_collection = MongoClient('mongodb://127.0.0.1:27017').logs.nginx
    log_stats(nginx_collection)
