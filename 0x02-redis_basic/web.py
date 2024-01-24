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
    def wrapper(url):  # sourcery skip: use-named-expression
        """ Wrapper for decorator """
        s_redis.incr(f"count:{url}")
        cached_html = s_redis.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')
        html = method(url)
        s_redis.setex(f"cached:{url}", 10, html)
        return html

    return wrapper


@count_url_response
def get_page(url: str) -> str:
    """
        Return HTML content
    """
    resp = requests.get(url)
    return resp.text
