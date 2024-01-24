#!/usr/bin/env python3
""" Operations of MongoDB with Python using pymongo """


def update_topics(mongo_collection, name, topics):
    """ Changes all topics of a school document based on the name """
    qry = {"name": name}
    new_vals = {"$set": {"topics": topics}}

    mongo_collection.update_many(qry, new_vals)
