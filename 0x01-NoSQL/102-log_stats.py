#!/usr/bin/env python3
""" Module: Improved log stats module """
from pymongo import MongoClient


def nginx_stats_check():
    """ function that provides some stats about Nginx logs stored in MongoDB:"""
    clnt = MongoClient()
    collection = clnt.logs.nginx

    count_of_docs = collection.count_documents({})
    print("{} logs".format(count_of_docs))
    print("Methods:")
    METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in METHODS:
        method_count = collection.count_documents({"method": method})
        print("\tmethod {}: {}".format(method, method_count))
    state = collection.count_documents({"method": "GET", "path": "/status"})
    print("{} status check".format(state))

    print("IPs:")

    top_IPs = collection.aggregate([
        {"$group":
         {
             "_id": "$ip",
             "count": {"$sum": 1}
         }
         },
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {"$project": {
            "_id": 0,
            "ip": "$_id",
            "count": 1
        }}
    ])
    for ip in top_IPs:
        num_count = ip.get("count")
        ip_address = ip.get("ip")
        print("\t{}: {}".format(ip_address, num_count))


if __name__ == "__main__":
    nginx_stats_check()
