#!/usr/bin/env python3
"""
Module for web cache and tracker
"""
import requests
import redis
from functools import wraps

store = redis.Redis()


def count_url_access(method):
    """ 
        Decorator counting how many times URL is accessed 
    """
    @wraps(method)
    def wrapper(url):
        cached = "cached:" + url
        cached_dt = store.get(cached)
        if cached_dt:
            return cached_dt.decode("utf-8")

        html = method(url)
        count = "count:" + url

        store.incr(count)
        store.set(cached, html)
        store.expire(cached, 10)
        return html
    return wrapper


@count_url_access
def get_page(url: str) -> str:
    """
        Module returns HTML content of url
    """
    return requests.get(url).text
