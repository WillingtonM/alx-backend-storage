#!/usr/bin/env python3
"""
Module for web cache and tracker
"""
from datetime import timedelta
from typing import Callable
import requests
from functools import wraps
import redis

s_redis = redis.Redis()


def count_url_response(method: Callable):
    """
        Decorator counting how many times URL is accessed
    """

    @wraps(method)
    def wrapper(url):
        cached_key = "cached:" + url
        cached_data = s_redis.get(cached_key)
        if cached_data:
            return cached_data.decode("utf-8")

        count_key = "count:" + url
        html = method(url)

        s_redis.incr(count_key)
        s_redis.set(cached_key, html)
        s_redis.expire(cached_key, 10)
        return html
    return wrapper


@count_url_response
def get_page(url: str) -> str:
    """
        Return HTML content
    """
    resp = requests.get(url)
    return resp.text
