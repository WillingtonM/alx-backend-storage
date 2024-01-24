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
        """wrapper function"""
        key = "cached:" + url
        cached_value = s_redis.get(key)
        if cached_value:
            return cached_value.decode("utf-8")

            # Get new content and update cache
        key_count = "count:" + url
        html_content = method(url)

        s_redis.incr(key_count)
        s_redis.set(key, html_content, ex=10)
        s_redis.expire(key, 10)
        return html_content
    return wrapper


@count_url_response
def get_page(url: str) -> str:
    """
        Return HTML content
    """
    return requests.get(url).text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
