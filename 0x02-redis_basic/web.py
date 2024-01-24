#!/usr/bin/env python3
"""
Module for web cache and tracker
"""
from datetime import timedelta
from typing import Callable
import requests
from functools import wraps
import redis


def count_url_response(method: Callable):
    """ 
        Decorator counting how many times URL is accessed 
    """

    @wraps(method)
    def wrapper(url: str, *args, **kwargs):
        """
            function that implement caching and tracking
        """
        key_count = "count:{}".format(url)
        redis = redis.Redis()
        redis.incr(key_count)
        res = method(url, *args, **kwargs)
        redis.setex(url, timedelta(seconds=10), str(res))
        return res

    return wrapper


@count_url_response
def get_page(url: str) -> str:
    """
        Return HTML content
    """
    response = requests.get(url)
    return response.text
